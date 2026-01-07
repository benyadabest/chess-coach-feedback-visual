"""
LangFuse Feedback & Performance Dashboard
Analyzes user feedback, failure categories, and trace performance metrics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ast
from datetime import datetime

st.set_page_config(
    page_title="LangFuse Feedback Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #334155;
    }
    .positive { color: #10b981; }
    .negative { color: #ef4444; }
    .neutral { color: #94a3b8; }
    .stMetric > div { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ============ DATA LOADING ============

@st.cache_data
def load_scores_data():
    """Load and process the scores export data."""
    scores_data = [
        {"id": "user_feedback_U095XD7U9M0_e29cbc90d6e061a5377cdadef140fc8a", "traceId": "e29cbc90d6e061a5377cdadef140fc8a", "timestamp": "2026-01-06T12:07:39.974Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U095XD7U9M0", "channel": "C0A4SNLDKHQ"},
        {"id": "user_feedback_U02NA9HP8G7_a54494e272057a3bc894e6c15cc2b107", "traceId": "a54494e272057a3bc894e6c15cc2b107", "timestamp": "2026-01-05T19:49:00.675Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U02NA9HP8G7", "channel": "C09T1KE0Y9G"},
        {"id": "user_feedback_U09A7KBFQSK_0985e25f246ed043594d4fcef0b795e3", "traceId": "0985e25f246ed043594d4fcef0b795e3", "timestamp": "2026-01-05T19:31:39.392Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U09A7KBFQSK", "channel": "C0A4SNLDKHQ"},
        {"id": "failure_unhelpful_U01QYGRC0FJ_fd6b20845dfdbd73a6efc1afa5e8e380", "traceId": "fd6b20845dfdbd73a6efc1afa5e8e380", "timestamp": "2026-01-05T18:42:09.226Z", "name": "failure_unhelpful", "value": 1, "comment": "the only real actionable here is 2: - Analyze games with a focus on space control and endgame techniques.\nbut the actionable on how to do this is vague and unhelpful\n\n(1 and 3 are because I play bullet - not real issues because I still convert those games, just in a suboptimal way)", "userId": "U01QYGRC0FJ", "channel": ""},
        {"id": "user_feedback_U01QYGRC0FJ_fd6b20845dfdbd73a6efc1afa5e8e380", "traceId": "fd6b20845dfdbd73a6efc1afa5e8e380", "timestamp": "2026-01-05T18:40:46.278Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U01QYGRC0FJ", "channel": "C09T1KE0Y9G"},
        {"id": "failure_other_U03V20RB4SV_f178dc3e55e9e2b8fbc848ae3d59d7c9", "traceId": "f178dc3e55e9e2b8fbc848ae3d59d7c9", "timestamp": "2026-01-02T14:56:30.287Z", "name": "failure_other", "value": 1, "comment": "Error when running game review", "userId": "U03V20RB4SV", "channel": ""},
        {"id": "user_feedback_U03V20RB4SV_f178dc3e55e9e2b8fbc848ae3d59d7c9", "traceId": "f178dc3e55e9e2b8fbc848ae3d59d7c9", "timestamp": "2026-01-02T14:55:51.547Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U03V20RB4SV", "channel": "C0A4SNLDKHQ"},
        {"id": "user_feedback_U05BWUL4STS_adb051534fd6f9ee8cbe137cec9bc419", "traceId": "adb051534fd6f9ee8cbe137cec9bc419", "timestamp": "2025-12-28T00:15:58.890Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U05BWUL4STS", "channel": "C0A4SNLDKHQ"},
        {"id": "failure_poor_format_U0VPTBY9F_a16b8b2680e9bdcdb05b54415fe1641d", "traceId": "a16b8b2680e9bdcdb05b54415fe1641d", "timestamp": "2025-12-26T20:23:39.829Z", "name": "failure_poor_format", "value": 1, "comment": "", "userId": "U0VPTBY9F", "channel": ""},
        {"id": "user_feedback_U0VPTBY9F_a16b8b2680e9bdcdb05b54415fe1641d", "traceId": "a16b8b2680e9bdcdb05b54415fe1641d", "timestamp": "2025-12-26T20:23:16.271Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0VPTBY9F", "channel": "C09T1KE0Y9G"},
        {"id": "failure_other_U08V8GVK571_380d222aa5a946101712ca6dfb3ff777", "traceId": "380d222aa5a946101712ca6dfb3ff777", "timestamp": "2025-12-26T19:18:27.144Z", "name": "failure_other", "value": 1, "comment": "testing", "userId": "U08V8GVK571", "channel": ""},
        {"id": "user_feedback_U08V8GVK571_380d222aa5a946101712ca6dfb3ff777", "traceId": "380d222aa5a946101712ca6dfb3ff777", "timestamp": "2025-12-26T19:17:17.248Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U0A4VQNLUM9_1766762488.804159", "traceId": "1766762488.804159", "timestamp": "2025-12-26T15:21:30.109Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766761231.634569", "traceId": "1766761231.634569", "timestamp": "2025-12-26T15:00:32.713Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766761125.829589", "traceId": "1766761125.829589", "timestamp": "2025-12-26T14:58:46.975Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U060K0B6TNE_1766287812.010219", "traceId": "1766287812.010219", "timestamp": "2025-12-26T10:41:22.075Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U060K0B6TNE", "channel": "C0ARC3TSB"},
        {"id": "user_feedback_U04RSKLP6QZ_1766679766.342299", "traceId": "1766679766.342299", "timestamp": "2025-12-25T16:26:11.196Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U04RSKLP6QZ", "channel": "C0A4SNLDKHQ"},
        {"id": "user_feedback_U09JDLGLH1C_1766637438.773629", "traceId": "1766637438.773629", "timestamp": "2025-12-25T04:37:19.800Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09JDLGLH1C", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09JDLGLH1C_1766637341.237559", "traceId": "1766637341.237559", "timestamp": "2025-12-25T04:35:42.606Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09JDLGLH1C", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U08V8GVK571_1766620257.713009", "traceId": "1766620257.713009", "timestamp": "2025-12-24T23:51:03.041Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766620249.394819", "traceId": "1766620249.394819", "timestamp": "2025-12-24T23:50:55.000Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766620235.139789", "traceId": "1766620235.139789", "timestamp": "2025-12-24T23:50:43.006Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766620191.945049", "traceId": "1766620191.945049", "timestamp": "2025-12-24T23:50:19.244Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U09JDLGLH1C_1766620191.945049", "traceId": "1766620191.945049", "timestamp": "2025-12-24T23:49:53.102Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09JDLGLH1C", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766618443.684439", "traceId": "1766618443.684439", "timestamp": "2025-12-24T23:20:54.255Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766618443.684439", "traceId": "1766618443.684439", "timestamp": "2025-12-24T23:20:45.199Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U09V1AJLZH9_1766618302.690269", "traceId": "1766618302.690269", "timestamp": "2025-12-24T23:18:29.936Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09V1AJLZH9", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09V1AJLZH9_1766618247.250559", "traceId": "1766618247.250559", "timestamp": "2025-12-24T23:17:33.023Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09V1AJLZH9", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09JDLGLH1C_1766618247.250559", "traceId": "1766618247.250559", "timestamp": "2025-12-24T23:17:28.751Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09JDLGLH1C", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U04ML73J2E5_1766609932.568329", "traceId": "1766609932.568329", "timestamp": "2025-12-24T22:50:56.400Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U04ML73J2E5", "channel": "C0A4SNLDKHQ"},
        {"id": "user_feedback_U08V8GVK571_1766615147.609479", "traceId": "1766615147.609479", "timestamp": "2025-12-24T22:38:05.068Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U08V8GVK571_1766615068.141649", "traceId": "1766615068.141649", "timestamp": "2025-12-24T22:37:59.381Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09V1AJLZH9_1766615147.609479", "traceId": "1766615147.609479", "timestamp": "2025-12-24T22:25:52.105Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09V1AJLZH9", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09V1AJLZH9_1766615068.141649", "traceId": "1766615068.141649", "timestamp": "2025-12-24T22:24:39.323Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09V1AJLZH9", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09JDLGLH1C_1766615068.141649", "traceId": "1766615068.141649", "timestamp": "2025-12-24T22:24:29.371Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09JDLGLH1C", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09V1AJLZH9_1766614681.067049", "traceId": "1766614681.067049", "timestamp": "2025-12-24T22:18:07.088Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09V1AJLZH9", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09V1AJLZH9_1766614548.609599", "traceId": "1766614548.609599", "timestamp": "2025-12-24T22:15:57.008Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09V1AJLZH9", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09JDLGLH1C_1766614548.609599", "traceId": "1766614548.609599", "timestamp": "2025-12-24T22:15:49.793Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09JDLGLH1C", "channel": "C0A2PGS5C92"},
        {"id": "failure_hallucinated_U054WK6J3C5_1766609932.568329", "traceId": "1766609932.568329", "timestamp": "2025-12-24T21:39:08.389Z", "name": "failure_hallucinated", "value": 1, "comment": "", "userId": "U054WK6J3C5", "channel": ""},
        {"id": "failure_incorrect_chess_U054WK6J3C5_1766609932.568329", "traceId": "1766609932.568329", "timestamp": "2025-12-24T21:39:08.389Z", "name": "failure_incorrect_chess", "value": 1, "comment": "", "userId": "U054WK6J3C5", "channel": ""},
        {"id": "user_feedback_U054WK6J3C5_1766609932.568329", "traceId": "1766609932.568329", "timestamp": "2025-12-24T21:38:46.522Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U054WK6J3C5", "channel": "C0A4SNLDKHQ"},
        {"id": "user_feedback_U08V8GVK571_1766611799.623289", "traceId": "1766611799.623289", "timestamp": "2025-12-24T21:30:04.462Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09V1AJLZH9_1766610784.421319", "traceId": "1766610784.421319", "timestamp": "2025-12-24T21:13:36.156Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09V1AJLZH9", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U08V8GVK571_1766610753.497239", "traceId": "1766610753.497239", "timestamp": "2025-12-24T21:12:48.153Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U08V8GVK571_1766610729.081179", "traceId": "1766610729.081179", "timestamp": "2025-12-24T21:12:15.485Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766610360.058439", "traceId": "1766610360.058439", "timestamp": "2025-12-24T21:06:11.619Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766609932.568329", "traceId": "1766609932.568329", "timestamp": "2025-12-24T20:59:24.033Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A4SNLDKHQ"},
        {"id": "user_feedback_U09V1AJLZH9_1766609932.568329", "traceId": "1766609932.568329", "timestamp": "2025-12-24T20:59:13.245Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09V1AJLZH9", "channel": "C0A4SNLDKHQ"},
        {"id": "user_feedback_U08V8GVK571_1766609455.089259", "traceId": "1766609455.089259", "timestamp": "2025-12-24T20:51:09.636Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09JDLGLH1C_1766609455.089259", "traceId": "1766609455.089259", "timestamp": "2025-12-24T20:50:56.362Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09JDLGLH1C", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U08V8GVK571_1766609228.565309", "traceId": "1766609228.565309", "timestamp": "2025-12-24T20:47:18.670Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09JDLGLH1C_1766609228.565309", "traceId": "1766609228.565309", "timestamp": "2025-12-24T20:47:09.852Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U09JDLGLH1C", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U0A4VQNLUM9_1766607394.014769", "traceId": "1766607394.014769", "timestamp": "2025-12-24T20:16:35.087Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766607316.573539", "traceId": "1766607316.573539", "timestamp": "2025-12-24T20:16:03.793Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766604762.007359", "traceId": "1766604762.007359", "timestamp": "2025-12-24T19:37:56.275Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U054WK6J3C5_1766604762.007359", "traceId": "1766604762.007359", "timestamp": "2025-12-24T19:36:26.122Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U054WK6J3C5", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09V1AJLZH9_1766604762.007359", "traceId": "1766604762.007359", "timestamp": "2025-12-24T19:32:50.127Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09V1AJLZH9", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U09JDLGLH1C_1766604762.007359", "traceId": "1766604762.007359", "timestamp": "2025-12-24T19:32:42.966Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U09JDLGLH1C", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U0A4VQNLUM9_1766599726.102109", "traceId": "1766599726.102109", "timestamp": "2025-12-24T18:08:47.556Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766599668.485789", "traceId": "1766599668.485789", "timestamp": "2025-12-24T18:07:49.707Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766598850.807289", "traceId": "1766598850.807289", "timestamp": "2025-12-24T17:54:12.087Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766598668.292449", "traceId": "1766598668.292449", "timestamp": "2025-12-24T17:51:09.545Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766598591.928679", "traceId": "1766598591.928679", "timestamp": "2025-12-24T17:49:52.955Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766598573.705029", "traceId": "1766598573.705029", "timestamp": "2025-12-24T17:49:43.822Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766598573.705029", "traceId": "1766598573.705029", "timestamp": "2025-12-24T17:49:35.010Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766596755.599599", "traceId": "1766596755.599599", "timestamp": "2025-12-24T17:19:16.519Z", "name": "user_feedback", "value": 1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766596319.157909", "traceId": "1766596319.157909", "timestamp": "2025-12-24T17:16:46.226Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766596430.599889", "traceId": "1766596430.599889", "timestamp": "2025-12-24T17:14:45.331Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A2PGS5C92"},
        {"id": "user_feedback_U08V8GVK571_1766596315.582779", "traceId": "1766596315.582779", "timestamp": "2025-12-24T17:12:12.489Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766596319.157909", "traceId": "1766596319.157909", "timestamp": "2025-12-24T17:12:01.374Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766596158.971759", "traceId": "1766596158.971759", "timestamp": "2025-12-24T17:09:20.434Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766596101.582449", "traceId": "1766596101.582449", "timestamp": "2025-12-24T17:08:22.657Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766596058.815349", "traceId": "1766596058.815349", "timestamp": "2025-12-24T17:08:17.563Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U0A4VQNLUM9_1766596058.815349", "traceId": "1766596058.815349", "timestamp": "2025-12-24T17:07:40.298Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U0A4VQNLUM9", "channel": "C0A3U5GRB16"},
        {"id": "user_feedback_U08V8GVK571_1766595638.804059", "traceId": "1766595638.804059", "timestamp": "2025-12-24T17:01:31.811Z", "name": "user_feedback", "value": -1, "comment": "", "userId": "U08V8GVK571", "channel": "C0A3U5GRB16"},
    ]
    return pd.DataFrame(scores_data)


@st.cache_data
def load_traces_data():
    """Load traces data with performance metrics. Replace with CSV path in production."""
    # Simulated traces data based on the analysis
    # In production, load from: pd.read_csv("path/to/traces.csv")
    traces_data = {
        'total_traces': 126,
        'latency_mean': 12.71,
        'latency_median': 9.62,
        'latency_min': 2.04,
        'latency_max': 48.60,
        'latency_std': 8.90,
        'input_tokens_mean': 19231,
        'output_tokens_mean': 389,
        'total_tokens_mean': 19620,
        'total_tokens_sum': 2472140,
        'cost_mean': 0.0478,
        'cost_median': 0.0372,
        'cost_total': 5.98,
        'cost_min': 0.0142,
        'cost_max': 0.2020,
        # Stats by feedback type
        'positive_latency': 12.36,
        'positive_tokens': 15224,
        'positive_cost': 0.0408,
        'negative_latency': 16.21,
        'negative_tokens': 22828,
        'negative_cost': 0.0572,
        'no_feedback_latency': 12.54,
        'no_feedback_tokens': 19532,
        'no_feedback_cost': 0.0475,
        # Failure stats
        'failure_latency': 18.48,
        'failure_tokens': 24672,
        'failure_cost': 0.0633,
    }
    return traces_data


def process_scores_data(df):
    """Process scores data to extract feedback and failure information."""
    feedback_df = df[df['name'] == 'user_feedback'].copy()
    failures_df = df[df['name'].str.startswith('failure_')].copy()
    
    return feedback_df, failures_df


# ============ SIDEBAR ============

st.sidebar.title("📊 Dashboard Controls")

# Toggle for no-feedback assumption
assume_no_feedback_good = st.sidebar.toggle(
    "🟢 Assume no feedback = good",
    value=False,
    help="If enabled, traces without feedback (57) are counted as positive"
)

# Filter by failure category
st.sidebar.subheader("Filter by Failure Type")
failure_types = ['All', 'hallucinated', 'incorrect_chess', 'other', 'poor_format', 'unhelpful']
selected_failure = st.sidebar.selectbox("Failure Category", failure_types)

# Date range info
st.sidebar.markdown("---")
st.sidebar.info("📅 **Data Range:** Dec 24, 2025 - Jan 6, 2026\n\n🔢 **Total Queries:** 126")


# ============ MAIN CONTENT ============

st.title("🎯 LangFuse Feedback & Performance Dashboard")
st.markdown("Analyzing user feedback, failure categories, latency, tokens, and costs.")

# Load data
scores_df = load_scores_data()
traces_data = load_traces_data()
feedback_df, failures_df = process_scores_data(scores_df)

# Calculate metrics
total_queries = 126
total_feedback = len(feedback_df)
positive_feedback = len(feedback_df[feedback_df['value'] == 1])
negative_feedback = len(feedback_df[feedback_df['value'] == -1])
no_feedback_count = total_queries - len(feedback_df['traceId'].unique())  # Unique traces with feedback

# Adjust for toggle
if assume_no_feedback_good:
    adjusted_positive = positive_feedback + 57  # 126 - 69 unique traces with feedback
    adjusted_total = total_feedback + 57
    satisfaction_rate = (adjusted_positive / adjusted_total) * 100
    display_positive = adjusted_positive
    display_total = adjusted_total
else:
    satisfaction_rate = (positive_feedback / total_feedback) * 100 if total_feedback > 0 else 0
    display_positive = positive_feedback
    display_total = total_feedback

# ============ KPI SECTION ============

st.header("📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Queries",
        total_queries,
        help="Total traces in the 14-day period"
    )

with col2:
    delta_color = "normal" if satisfaction_rate >= 50 else "inverse"
    st.metric(
        "Satisfaction Rate",
        f"{satisfaction_rate:.1f}%",
        delta=f"+57 assumed good" if assume_no_feedback_good else None,
        delta_color=delta_color
    )

with col3:
    st.metric(
        "👍 Positive",
        display_positive,
        delta=f"+57" if assume_no_feedback_good else None,
        delta_color="normal"
    )

with col4:
    st.metric(
        "👎 Negative",
        negative_feedback
    )

# Toggle explanation
if assume_no_feedback_good:
    st.success(f"✅ **No-feedback assumption enabled:** 57 queries without reactions are counted as positive (126 total - 69 with feedback = 57 silent)")

# ============ PERFORMANCE METRICS ============

st.header("⚡ Performance Metrics")

perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)

with perf_col1:
    st.metric("Avg Latency", f"{traces_data['latency_mean']:.2f}s", help="Mean response time")
    st.caption(f"Median: {traces_data['latency_median']:.2f}s")

with perf_col2:
    st.metric("Avg Tokens", f"{traces_data['total_tokens_mean']:,.0f}", help="Mean tokens per request")
    st.caption(f"Total: {traces_data['total_tokens_sum']:,.0f}")

with perf_col3:
    st.metric("Avg Cost", f"${traces_data['cost_mean']:.4f}", help="Mean cost per request")
    st.caption(f"Total: ${traces_data['cost_total']:.2f}")

with perf_col4:
    st.metric("Total Failures", len(failures_df['traceId'].unique()), help="Unique traces with failure tags")

# ============ PERFORMANCE BY FEEDBACK TYPE ============

st.subheader("📊 Performance by Feedback Type")

perf_comparison = pd.DataFrame({
    'Feedback Type': ['👍 Positive', '👎 Negative', '❓ No Feedback', '⚠️ With Failures'],
    'Avg Latency (s)': [traces_data['positive_latency'], traces_data['negative_latency'], 
                        traces_data['no_feedback_latency'], traces_data['failure_latency']],
    'Avg Tokens': [traces_data['positive_tokens'], traces_data['negative_tokens'],
                   traces_data['no_feedback_tokens'], traces_data['failure_tokens']],
    'Avg Cost ($)': [traces_data['positive_cost'], traces_data['negative_cost'],
                     traces_data['no_feedback_cost'], traces_data['failure_cost']]
})

# Create comparison chart
fig_perf = make_subplots(rows=1, cols=3, subplot_titles=['Latency (s)', 'Tokens', 'Cost ($)'])

colors = ['#10b981', '#ef4444', '#6b7280', '#f59e0b']

fig_perf.add_trace(
    go.Bar(x=perf_comparison['Feedback Type'], y=perf_comparison['Avg Latency (s)'], 
           marker_color=colors, name='Latency'),
    row=1, col=1
)
fig_perf.add_trace(
    go.Bar(x=perf_comparison['Feedback Type'], y=perf_comparison['Avg Tokens'], 
           marker_color=colors, name='Tokens'),
    row=1, col=2
)
fig_perf.add_trace(
    go.Bar(x=perf_comparison['Feedback Type'], y=perf_comparison['Avg Cost ($)'], 
           marker_color=colors, name='Cost'),
    row=1, col=3
)

fig_perf.update_layout(height=350, showlegend=False, template='plotly_dark')
st.plotly_chart(fig_perf, use_container_width=True)

st.info("💡 **Insight:** Negative feedback correlates with **higher latency** (+31%), **more tokens** (+50%), and **higher cost** (+40%) compared to positive feedback.")

# ============ FAILURE ANALYSIS ============

st.header("🚨 Failure Analysis")

# Count failures by type
failure_counts = failures_df['name'].str.replace('failure_', '').value_counts()
failure_dict = failure_counts.to_dict()

# Filter logic
if selected_failure != 'All':
    filtered_failures = failures_df[failures_df['name'] == f'failure_{selected_failure}']
    st.info(f"🔍 Showing {len(filtered_failures)} entries for **{selected_failure}** failures")
else:
    filtered_failures = failures_df

col1, col2 = st.columns(2)

with col1:
    st.subheader("Failure Distribution")
    if len(failure_counts) > 0:
        fig_failures = px.pie(
            values=list(failure_dict.values()),
            names=[k.replace('_', ' ').title() for k in failure_dict.keys()],
            color_discrete_sequence=['#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#f97316'],
            hole=0.4
        )
        fig_failures.update_layout(template='plotly_dark', height=300)
        st.plotly_chart(fig_failures, use_container_width=True)
    else:
        st.write("No failures recorded")

with col2:
    st.subheader("Failure Counts")
    for failure_type, count in failure_dict.items():
        display_name = failure_type.replace('_', ' ').title()
        st.markdown(f"**{display_name}:** {count}")
    
    st.markdown("---")
    st.markdown(f"**Total Failure Tags:** {len(failures_df)}")
    st.markdown(f"**Unique Traces with Failures:** {failures_df['traceId'].nunique()}")

# Failure comments
st.subheader("📝 Failure Comments")
comments = filtered_failures[filtered_failures['comment'].str.len() > 0]
if len(comments) > 0:
    for _, row in comments.iterrows():
        failure_type = row['name'].replace('failure_', '').replace('_', ' ').title()
        st.warning(f"**{failure_type}** — {row['timestamp'][:10]}")
        st.markdown(f"> {row['comment']}")
else:
    st.info("No comments available for selected failures")

# ============ FEEDBACK BY USER & CHANNEL ============

st.header("👥 Feedback by User & Channel")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Users by Feedback Volume")
    user_feedback = feedback_df.groupby('userId').agg(
        positive=('value', lambda x: (x == 1).sum()),
        negative=('value', lambda x: (x == -1).sum())
    ).reset_index()
    user_feedback['total'] = user_feedback['positive'] + user_feedback['negative']
    user_feedback = user_feedback.sort_values('total', ascending=False).head(8)
    
    fig_users = go.Figure()
    fig_users.add_trace(go.Bar(
        name='Positive', x=user_feedback['userId'].str[-6:], y=user_feedback['positive'],
        marker_color='#10b981'
    ))
    fig_users.add_trace(go.Bar(
        name='Negative', x=user_feedback['userId'].str[-6:], y=user_feedback['negative'],
        marker_color='#ef4444'
    ))
    fig_users.update_layout(barmode='stack', template='plotly_dark', height=300)
    st.plotly_chart(fig_users, use_container_width=True)

with col2:
    st.subheader("Feedback by Channel")
    channel_names = {
        'C0A4SNLDKHQ': 'Main',
        'C09T1KE0Y9G': 'Support',
        'C0A2PGS5C92': 'Testing',
        'C0A3U5GRB16': 'Dev',
        'C0ARC3TSB': 'General',
    }
    
    channel_feedback = feedback_df[feedback_df['channel'] != ''].groupby('channel').agg(
        positive=('value', lambda x: (x == 1).sum()),
        negative=('value', lambda x: (x == -1).sum())
    ).reset_index()
    channel_feedback['name'] = channel_feedback['channel'].map(channel_names).fillna(channel_feedback['channel'].str[-4:])
    
    fig_channels = go.Figure()
    fig_channels.add_trace(go.Bar(
        name='Positive', x=channel_feedback['name'], y=channel_feedback['positive'],
        marker_color='#10b981'
    ))
    fig_channels.add_trace(go.Bar(
        name='Negative', x=channel_feedback['name'], y=channel_feedback['negative'],
        marker_color='#ef4444'
    ))
    fig_channels.update_layout(barmode='stack', template='plotly_dark', height=300)
    st.plotly_chart(fig_channels, use_container_width=True)

# ============ DAILY TREND ============

st.header("📅 Daily Feedback Trend")

feedback_df['date'] = pd.to_datetime(feedback_df['timestamp']).dt.date
daily = feedback_df.groupby('date').agg(
    positive=('value', lambda x: (x == 1).sum()),
    negative=('value', lambda x: (x == -1).sum())
).reset_index()

fig_daily = go.Figure()
fig_daily.add_trace(go.Bar(name='Positive', x=daily['date'], y=daily['positive'], marker_color='#10b981'))
fig_daily.add_trace(go.Bar(name='Negative', x=daily['date'], y=daily['negative'], marker_color='#ef4444'))
fig_daily.update_layout(barmode='stack', template='plotly_dark', height=300, xaxis_title='Date', yaxis_title='Feedback Count')
st.plotly_chart(fig_daily, use_container_width=True)

# ============ SUMMARY ============

st.header("📋 Summary & Recommendations")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.subheader("Key Findings")
    if assume_no_feedback_good:
        st.markdown(f"""
        - **Adjusted satisfaction rate: {satisfaction_rate:.1f}%** (with no-feedback = good)
        - Original rate without assumption: {(positive_feedback/total_feedback)*100:.1f}%
        - **57 queries** had no user reaction
        """)
    else:
        st.markdown(f"""
        - **Low satisfaction rate: {satisfaction_rate:.1f}%**
        - Only {positive_feedback} positive vs {negative_feedback} negative feedback
        - **57 queries** had no user reaction (toggle above to count as positive)
        """)
    
    st.markdown(f"""
    - **{len(failure_dict)} failure categories** documented
    - Negative feedback correlates with higher latency/cost
    - Dec 24 had the highest volume of negative feedback
    """)

with summary_col2:
    st.subheader("Recommendations")
    st.markdown("""
    1. **Reduce latency** — Negative cases average 16.2s vs 12.4s for positive
    2. **Improve chess analysis accuracy** — Incorrect chess and hallucinations noted
    3. **Provide more specific advice** — "Unhelpful" feedback cited vague actionables
    4. **Standardize output formatting** — Poor format failures reported
    5. **Monitor Testing/Dev channels** — Highest negative feedback rates
    """)

# Footer
st.markdown("---")
st.caption("Dashboard built with Streamlit · Data from LangFuse exports")
