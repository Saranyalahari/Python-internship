# app.py
import streamlit as st
import subprocess
import tempfile
import os
import re
from pathlib import Path
import black
import flake8.api.legacy as flake8
import radon.complexity as radon_comp
import radon.metrics as radon_metrics
import radon.raw as radon_raw
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import sys

# Configure page
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .improvement-suggestion {
        background-color: #fff3e0;
        padding: 0.8rem;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
    }
    .good-practice {
        background-color: #e8f5e9;
        padding: 0.8rem;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    .error-highlight {
        background-color: #ffebee;
        padding: 0.8rem;
        border-left: 4px solid #f44336;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


class CodeAnalyzer:
    """Class to handle code analysis operations"""

    def __init__(self, code):
        self.code = code
        self.analysis_results = {}

    def run_flake8_analysis(self):
        """Run flake8 style analysis"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(self.code)
                temp_file = f.name

            style_guide = flake8.get_style_guide(
                ignore=['E501'],  # Ignore line length for now
                max_line_length=88
            )
            report = style_guide.check_files([temp_file])

            errors = []
            for error in report.get_statistics(''):
                errors.append(error)

            os.unlink(temp_file)
            return errors
        except Exception as e:
            return [f"Error running flake8: {str(e)}"]

    def run_black_check(self):
        """Check if code is formatted with black"""
        try:
            formatted_code = black.format_str(self.code, mode=black.Mode())
            if formatted_code.strip() != self.code.strip():
                return {
                    'is_formatted': False,
                    'formatted_code': formatted_code,
                    'differences': self._get_diff(self.code, formatted_code)
                }
            return {'is_formatted': True, 'formatted_code': self.code, 'differences': []}
        except Exception as e:
            return {'is_formatted': False, 'formatted_code': None, 'differences': [f"Error: {str(e)}"]}

    def _get_diff(self, original, formatted):
        """Get differences between original and formatted code"""
        original_lines = original.split('\n')
        formatted_lines = formatted.split('\n')
        differences = []

        for i, (orig, form) in enumerate(zip(original_lines, formatted_lines)):
            if orig != form:
                differences.append({
                    'line': i + 1,
                    'original': orig,
                    'formatted': form
                })
        return differences

    def analyze_complexity(self):
        """Analyze code complexity using radon"""
        try:
            # Cyclomatic complexity
            complexity = list(radon_comp.cc_visit(self.code))

            # Maintainability index
            mi = radon_metrics.mi_visit(self.code, False)

            # Raw metrics
            raw_metrics = radon_raw.analyze(self.code)

            # Classify complexity
            for item in complexity:
                if item.complexity <= 5:
                    item.risk = 'A - Low'
                elif item.complexity <= 10:
                    item.risk = 'B - Moderate'
                elif item.complexity <= 20:
                    item.risk = 'C - High'
                else:
                    item.risk = 'D - Very High'

            return {
                'cyclomatic_complexity': complexity,
                'maintainability_index': mi,
                'raw_metrics': {
                    'lines_of_code': raw_metrics.loc,
                    'logical_lines': raw_metrics.lloc,
                    'comments': raw_metrics.comments,
                    'blank_lines': raw_metrics.blank,
                    'single_comments': raw_metrics.single_comments
                }
            }
        except Exception as e:
            return {'error': str(e)}

    def identify_improvements(self, flake8_errors, complexity_results):
        """Identify specific improvements needed"""
        improvements = []

        # Style improvements from flake8
        style_issues = []
        for error in flake8_errors:
            if 'E' in str(error):  # Style errors
                style_issues.append(error)
            elif 'W' in str(error):  # Warnings
                style_issues.append(error)

        if style_issues:
            improvements.append({
                'category': 'Style Issues',
                'severity': 'Medium',
                'description': f'Found {len(style_issues)} style violations',
                'details': style_issues[:5]  # Show first 5
            })

        # Complexity improvements
        if complexity_results and 'cyclomatic_complexity' in complexity_results:
            high_complexity = [c for c in complexity_results['cyclomatic_complexity']
                               if c.complexity > 10]
            if high_complexity:
                improvements.append({
                    'category': 'High Complexity',
                    'severity': 'High',
                    'description': f'Found {len(high_complexity)} functions with high complexity',
                    'details': [f"{c.name}: complexity {c.complexity} ({c.risk})"
                                for c in high_complexity]
                })

        # Code quality metrics
        if complexity_results and 'raw_metrics' in complexity_results:
            raw = complexity_results['raw_metrics']
            if raw['comments'] < raw['logical_lines'] * 0.1:
                improvements.append({
                    'category': 'Documentation',
                    'severity': 'Medium',
                    'description': 'Low comment ratio',
                    'details': [f'Comments: {raw["comments"]}, Code lines: {raw["logical_lines"]}']
                })

        return improvements

    def calculate_quality_score(self):
        """Calculate overall quality score"""
        score = 100

        # Flake8 errors reduce score
        flake8_errors = self.run_flake8_analysis()
        score -= len(flake8_errors) * 2

        # Complexity penalties
        complexity = self.analyze_complexity()
        if complexity and 'cyclomatic_complexity' in complexity:
            for comp in complexity['cyclomatic_complexity']:
                if comp.complexity > 20:
                    score -= 10
                elif comp.complexity > 10:
                    score -= 5

        # Black formatting
        black_check = self.run_black_check()
        if not black_check['is_formatted']:
            score -= 10

        return max(0, min(100, score))


class CodeFormatter:
    """Class to handle code formatting"""

    @staticmethod
    def format_with_black(code):
        """Format code using black"""
        try:
            return black.format_str(code, mode=black.Mode())
        except Exception as e:
            return f"Error formatting: {str(e)}"

    @staticmethod
    def suggest_improvements(code):
        """Suggest specific code improvements"""
        suggestions = []

        # Check for common issues
        lines = code.split('\n')

        # Check line length
        for i, line in enumerate(lines):
            if len(line) > 88:
                suggestions.append({
                    'line': i + 1,
                    'issue': 'Line too long',
                    'suggestion': f'Line length {len(line)} > 88. Consider breaking it down.',
                    'original': line
                })

        # Check for unused imports (basic)
        import_pattern = re.compile(r'^import\s+(\w+)|^from\s+(\w+)\s+import')
        imports = []
        for i, line in enumerate(lines):
            if import_pattern.match(line.strip()):
                imports.append(line)

        # Check for missing docstrings (basic)
        has_docstring = False
        for line in lines[:20]:  # Check first 20 lines
            if '"""' in line or "'''" in line:
                has_docstring = True
                break

        if not has_docstring and len(lines) > 5:
            suggestions.append({
                'line': 1,
                'issue': 'Missing module docstring',
                'suggestion': 'Add a docstring at the beginning of the file explaining its purpose.',
                'original': ''
            })

        return suggestions


def create_visualization(analysis_data):
    """Create visualizations for code metrics"""

    # Complexity gauge
    if 'cyclomatic_complexity' in analysis_data:
        complexities = [c.complexity for c in analysis_data['cyclomatic_complexity']]
        avg_complexity = sum(complexities) / len(complexities) if complexities else 0

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_complexity,
            title={'text': "Average Cyclomatic Complexity"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 30]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 5], 'color': "lightgreen"},
                    {'range': [5, 10], 'color': "yellow"},
                    {'range': [10, 20], 'color': "orange"},
                    {'range': [20, 30], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 10
                }
            }
        ))

        return fig_gauge

    return None


def export_report(analysis_results, original_code, formatted_code):
    """Export analysis report in multiple formats"""

    report = {
        'timestamp': datetime.now().isoformat(),
        'quality_score': analysis_results['quality_score'],
        'summary': analysis_results['summary'],
        'metrics': analysis_results['metrics'],
        'improvements': analysis_results['improvements'],
        'code_comparison': {
            'original': original_code,
            'formatted': formatted_code
        }
    }

    # JSON report
    json_report = json.dumps(report, indent=2, default=str)

    # Markdown report
    md_report = f"""# Code Quality Analysis Report

## Overview
- **Timestamp**: {report['timestamp']}
- **Quality Score**: {report['quality_score']}/100

## Summary
{report['summary']}

## Metrics
- **Cyclomatic Complexity**: {report['metrics'].get('avg_complexity', 'N/A')}
- **Maintainability Index**: {report['metrics'].get('maintainability_index', 'N/A')}
- **Lines of Code**: {report['metrics'].get('lines_of_code', 'N/A')}
- **Comments**: {report['metrics'].get('comments', 'N/A')}

## Improvements Needed
"""

    for imp in report['improvements']:
        md_report += f"\n### {imp['category']} (Severity: {imp['severity']})\n"
        md_report += f"{imp['description']}\n"
        if 'details' in imp:
            for detail in imp['details'][:3]:
                md_report += f"- {detail}\n"

    return json_report, md_report


def main():
    """Main Streamlit application"""

    # Header
    st.markdown('<h1 class="main-header">🔍 AI Code Reviewer</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Analysis Settings")

        analysis_type = st.multiselect(
            "Select analysis types:",
            ["Style Check (flake8)", "Formatting (black)", "Complexity (radon)", "Improvement Suggestions"],
            default=["Style Check (flake8)", "Formatting (black)", "Complexity (radon)", "Improvement Suggestions"]
        )

        st.markdown("---")
        st.markdown("### 📊 Quality Thresholds")

        complexity_threshold = st.slider(
            "Max acceptable complexity:",
            min_value=5, max_value=20, value=10,
            help="Functions with complexity above this will be flagged"
        )

        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info("""
        This AI Code Reviewer analyzes Python code for:
        - Code style violations (flake8)
        - Formatting issues (black)
        - Complexity metrics (radon)
        - Improvement suggestions

        Upload your Python file or paste code to get started!
        """)

    # Main content area - two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📝 Input Code")

        # Input method selection
        input_method = st.radio("Choose input method:", ["Paste code", "Upload file"], horizontal=True)

        code_input = ""

        if input_method == "Paste code":
            code_input = st.text_area(
                "Paste your Python code here:",
                height=400,
                placeholder="def example_function():\n    print('Hello, World!')"
            )
        else:
            uploaded_file = st.file_uploader("Choose a Python file", type=['py'])
            if uploaded_file is not None:
                code_input = uploaded_file.getvalue().decode("utf-8")
                st.code(code_input, language='python')

        if not code_input:
            st.info("👈 Enter your Python code to start analysis")
            return

    # Perform analysis when code is provided
    if code_input:
        with st.spinner("Analyzing code..."):
            analyzer = CodeAnalyzer(code_input)
            formatter = CodeFormatter()

            # Run selected analyses
            analysis_results = {}
            improvements = []

            # Style analysis
            if "Style Check (flake8)" in analysis_type:
                flake8_errors = analyzer.run_flake8_analysis()
                analysis_results['flake8'] = flake8_errors

            # Formatting check
            if "Formatting (black)" in analysis_type:
                black_check = analyzer.run_black_check()
                analysis_results['black'] = black_check

            # Complexity analysis
            if "Complexity (radon)" in analysis_type:
                complexity_results = analyzer.analyze_complexity()
                analysis_results['complexity'] = complexity_results

            # Improvement suggestions
            if "Improvement Suggestions" in analysis_type:
                suggestions = formatter.suggest_improvements(code_input)
                improvements.extend(suggestions)

            # Quality score
            quality_score = analyzer.calculate_quality_score()

            # Get improvements from analysis
            if 'flake8' in analysis_results and 'complexity' in analysis_results:
                improvements_from_analysis = analyzer.identify_improvements(
                    analysis_results.get('flake8', []),
                    analysis_results.get('complexity', {})
                )
                improvements.extend(improvements_from_analysis)

            # Display results in second column
            with col2:
                st.markdown("### 📊 Analysis Results")

                # Quality score with progress bar
                st.markdown("#### Overall Quality Score")
                st.progress(quality_score / 100)
                st.markdown(f"**Score: {quality_score}/100**")

                # Summary metrics
                st.markdown("#### Key Metrics")
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

                with metrics_col1:
                    if 'complexity' in analysis_results and analysis_results['complexity']:
                        complexity_data = analysis_results['complexity']
                        if 'cyclomatic_complexity' in complexity_data:
                            avg_complexity = sum(c.complexity for c in complexity_data['cyclomatic_complexity']) / len(
                                complexity_data['cyclomatic_complexity']) if complexity_data[
                                'cyclomatic_complexity'] else 0
                            st.metric("Avg Complexity", f"{avg_complexity:.1f}")

                with metrics_col2:
                    if 'flake8' in analysis_results:
                        st.metric("Style Issues", len(analysis_results['flake8']))

                with metrics_col3:
                    if 'complexity' in analysis_results and analysis_results['complexity']:
                        if 'raw_metrics' in analysis_results['complexity']:
                            loc = analysis_results['complexity']['raw_metrics']['lines_of_code']
                            st.metric("Lines of Code", loc)

                # Complexity visualization
                if 'complexity' in analysis_results and 'cyclomatic_complexity' in analysis_results['complexity']:
                    fig = create_visualization(analysis_results['complexity'])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

                # Display improvements
                if improvements:
                    st.markdown("#### 💡 Improvement Suggestions")

                    for imp in improvements[:5]:  # Show top 5
                        if 'severity' in imp and imp['severity'] == 'High':
                            with st.expander(f"⚠️ {imp['category']} - {imp['severity']} Priority"):
                                st.write(imp['description'])
                                if 'details' in imp:
                                    for detail in imp['details'][:3]:
                                        st.write(f"- {detail}")
                        else:
                            with st.expander(f"📝 {imp['category']}"):
                                st.write(imp['description'])
                                if 'details' in imp:
                                    for detail in imp['details'][:3]:
                                        st.write(f"- {detail}")

                # Display flake8 issues
                if 'flake8' in analysis_results and analysis_results['flake8']:
                    with st.expander("🔍 Style Issues Details"):
                        for error in analysis_results['flake8'][:10]:
                            st.error(str(error))

            # Detailed analysis section
            st.markdown("---")
            st.markdown("### 🔧 Detailed Analysis")

            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(
                ["📝 Code Comparison", "📊 Complexity Details", "💡 All Suggestions", "📄 Export Report"])

            with tab1:
                if 'black' in analysis_results and not analysis_results['black']['is_formatted']:
                    st.markdown("#### Before/After Formatting")
                    col_left, col_right = st.columns(2)

                    with col_left:
                        st.markdown("**Original Code**")
                        st.code(code_input, language='python')

                    with col_right:
                        st.markdown("**Formatted with Black**")
                        if analysis_results['black']['formatted_code']:
                            st.code(analysis_results['black']['formatted_code'], language='python')
                            st.success("✓ Code can be improved with Black formatting")
                else:
                    st.success("✓ Code is already properly formatted with Black!")

            with tab2:
                if 'complexity' in analysis_results:
                    if 'cyclomatic_complexity' in analysis_results['complexity']:
                        st.markdown("#### Cyclomatic Complexity per Function")

                        complexity_data = []
                        for comp in analysis_results['complexity']['cyclomatic_complexity']:
                            complexity_data.append({
                                'Function': comp.name,
                                'Complexity': comp.complexity,
                                'Risk': comp.risk,
                                'Line': comp.lineno
                            })

                        if complexity_data:
                            df = pd.DataFrame(complexity_data)
                            st.dataframe(df, use_container_width=True)

                            # Highlight high complexity
                            high_complexity_functions = df[df['Complexity'] > complexity_threshold]
                            if not high_complexity_functions.empty:
                                st.warning(
                                    f"⚠️ {len(high_complexity_functions)} functions have complexity > {complexity_threshold}")

                    if 'maintainability_index' in analysis_results['complexity']:
                        mi = analysis_results['complexity']['maintainability_index']
                        st.markdown(f"**Maintainability Index:** {mi:.2f}")
                        if mi < 65:
                            st.warning("Low maintainability - consider refactoring")

            with tab3:
                if improvements:
                    st.markdown("#### All Improvement Suggestions")
                    for imp in improvements:
                        if 'line' in imp:
                            st.markdown(f"**Line {imp['line']}**: {imp['issue']}")
                            st.markdown(f"*Suggestion*: {imp['suggestion']}")
                            if imp['original']:
                                st.code(imp['original'], language='python')
                        else:
                            st.markdown(f"**{imp['category']}** ({imp['severity']})")
                            st.markdown(imp['description'])
                    st.markdown("---")
                else:
                    st.success("🎉 No major issues found! Your code looks good!")

            with tab4:
                st.markdown("#### Export Analysis Report")

                # Prepare report data
                report_data = {
                    'quality_score': quality_score,
                    'summary': f"Analysis complete. Quality score: {quality_score}/100",
                    'metrics': {
                        'avg_complexity': avg_complexity if 'complexity' in analysis_results else 'N/A',
                        'maintainability_index': analysis_results.get('complexity', {}).get('maintainability_index',
                                                                                            'N/A'),
                        'lines_of_code': analysis_results.get('complexity', {}).get('raw_metrics', {}).get(
                            'lines_of_code', 'N/A'),
                        'comments': analysis_results.get('complexity', {}).get('raw_metrics', {}).get('comments', 'N/A')
                    },
                    'improvements': improvements,
                    'analysis_results': analysis_results
                }

                json_report, md_report = export_report(
                    report_data,
                    code_input,
                    analysis_results.get('black', {}).get('formatted_code', code_input)
                )

                col_json, col_md = st.columns(2)

                with col_json:
                    st.download_button(
                        label="📥 Download JSON Report",
                        data=json_report,
                        file_name=f"code_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )

                with col_md:
                    st.download_button(
                        label="📥 Download Markdown Report",
                        data=md_report,
                        file_name=f"code_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )

                # Preview report
                with st.expander("Preview Report"):
                    st.markdown(md_report[:1000] + "..." if len(md_report) > 1000 else md_report)


if __name__ == "__main__":
    main()