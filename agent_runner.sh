#!/bin/bash
# BagajPark Growth Agent Runner
# Runs all growth agents and produces reports
set -e

REPORT_DIR="reports"
mkdir -p "$REPORT_DIR"

echo "=========================================="
echo "  BagajPark Growth Agent Suite"
echo "  $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "=========================================="

run_agent() {
    local name="$1"
    local script="$2"
    echo ""
    echo "── Running $name ──"
    if python3 "$script" 2>&1; then
        echo "✅ $name completed"
    else
        echo "❌ $name failed" >&2
    fi
}

# Existing agents
run_agent "Competitor Scanner" "agents/competitor_scanner.py"
run_agent "Blog Engine" "agents/blog_engine.py"
run_agent "Reddit Monitor" "agents/reddit_monitor.py"
run_agent "App Review Analyzer" "agents/app_review_analyzer.py"

# New SEO & growth agents
run_agent "SEO Content Generator" "agents/seo_content_generator.py"
run_agent "Blog Auto-Publisher" "agents/blog_auto_publisher.py"
run_agent "Backlink Scout" "agents/backlink_scout.py"

echo ""
echo "=========================================="
echo "  Reports generated in $REPORT_DIR/"
ls -lh "$REPORT_DIR/" 2>/dev/null || echo "  (no reports yet)"
echo "=========================================="
