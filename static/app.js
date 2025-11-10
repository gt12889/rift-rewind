const API_BASE = 'http://localhost:8000';

async function getInsights() {
    const summonerName = document.getElementById('summonerName').value.trim();
    const region = document.getElementById('region').value;
    const actionType = document.getElementById('actionType').value;
    
    if (!summonerName) {
        showError('Please enter a summoner name in format: GameName#Tag');
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('error').style.display = 'none';
    document.getElementById('results').style.display = 'none';
    
    try {
        let url;
        if (actionType === 'insights') {
            url = `${API_BASE}/api/player/${encodeURIComponent(summonerName)}/insights?region=${region}&match_count=50`;
        } else if (actionType === 'year-summary') {
            url = `${API_BASE}/api/player/${encodeURIComponent(summonerName)}/year-summary?year=2024&region=${region}`;
        } else if (actionType === 'social-content') {
            url = `${API_BASE}/api/player/${encodeURIComponent(summonerName)}/social-content?content_type=year-end&region=${region}`;
        }
        
        const response = await fetch(url);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch insights');
        }
        
        const data = await response.json();
        displayResults(data, actionType);
        
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function displayResults(data, actionType) {
    if (actionType === 'insights') {
        // Display insights
        let metricsHtml = '';
        if (data.rank_info) {
            metricsHtml += formatRankInfo(data.rank_info);
            metricsHtml += '<hr style="margin: 15px 0;">';
        }
        metricsHtml += formatKeyMetrics(data.key_metrics || {});
        document.getElementById('keyMetrics').innerHTML = metricsHtml;
        document.getElementById('trends').textContent = data.trends || 'No trend data available';
        
        document.getElementById('strengthsList').innerHTML = formatList(data.strengths || [], 'strength');
        document.getElementById('weaknessesList').innerHTML = formatList(data.weaknesses || [], 'weakness');
        document.getElementById('insightsList').innerHTML = formatList(data.unexpected_insights || [], 'insight-item');
        document.getElementById('recommendationsList').innerHTML = formatList(data.recommendations || [], 'insight-item');
    } else if (actionType === 'year-summary') {
        // Display year summary
        document.getElementById('keyMetrics').innerHTML = formatYearSummary(data.summary || {});
        document.getElementById('trends').textContent = data.ai_generated_summary || 'No summary available';
        
        document.getElementById('strengthsList').innerHTML = formatList(data.strengths || [], 'strength');
        document.getElementById('weaknessesList').innerHTML = formatList(data.weaknesses || [], 'weakness');
        document.getElementById('insightsList').innerHTML = formatHighlights(data.highlights || []);
        document.getElementById('recommendationsList').innerHTML = formatList(data.growth_areas || [], 'insight-item');
    } else if (actionType === 'social-content') {
        // Display social content
        document.getElementById('keyMetrics').innerHTML = formatSocialContent(data);
        document.getElementById('trends').textContent = data.share_text || 'No content available';
    }
    
    document.getElementById('results').style.display = 'block';
}

function formatRankInfo(rankInfo) {
    if (!rankInfo) return '';
    
    let html = '<div class="rank-badge">';
    
    if (rankInfo.solo_queue) {
        const sq = rankInfo.solo_queue;
        html += `
            <p style="font-size: 1.2em; margin-bottom: 10px;"><strong>🏆 ${sq.tier} ${sq.rank}</strong></p>
            <p><strong>${sq.league_points} LP</strong> • Win Rate: ${sq.win_rate.toFixed(1)}% (${sq.wins}W / ${sq.losses}L)</p>
            ${sq.hot_streak ? '<p style="color: #ffeb3b;">🔥 Hot Streak Active!</p>' : ''}
        `;
    } else {
        html += '<p>Unranked</p>';
    }
    
    html += '</div>';
    return html;
}

function formatKeyMetrics(metrics) {
    if (!metrics || Object.keys(metrics).length === 0) {
        return '<p>No metrics available</p>';
    }
    
    return `
        <p><strong>Average KDA:</strong> ${metrics.avg_kda?.toFixed(2) || 'N/A'}</p>
        <p><strong>Average Damage:</strong> ${metrics.avg_damage?.toLocaleString() || 'N/A'}</p>
        <p><strong>Average Gold:</strong> ${metrics.avg_gold?.toLocaleString() || 'N/A'}</p>
        <p><strong>Average Vision Score:</strong> ${metrics.avg_vision_score?.toFixed(1) || 'N/A'}</p>
        <p><strong>Average CS:</strong> ${metrics.avg_cs?.toFixed(1) || 'N/A'}</p>
    `;
}

function formatYearSummary(summary) {
    return `
        <p><strong>Total Games:</strong> ${summary.total_games || 0}</p>
        <p><strong>Win Rate:</strong> ${summary.win_rate?.toFixed(1) || 0}%</p>
        <p><strong>Most Played Champion:</strong> ${summary.best_champion || 'N/A'}</p>
    `;
}

function formatSocialContent(data) {
    if (data.stats) {
        return `
            <p><strong>Total Games:</strong> ${data.stats.total_games || 0}</p>
            <p><strong>Win Rate:</strong> ${data.stats.win_rate || 'N/A'}</p>
            <p><strong>Most Played:</strong> ${data.stats.most_played || 'N/A'}</p>
        `;
    }
    return '<p>No content available</p>';
}

function formatList(items, className) {
    if (!items || items.length === 0) {
        return '<p>No items available</p>';
    }
    
    return items.map(item => 
        `<div class="${className}">${item}</div>`
    ).join('');
}

function formatHighlights(highlights) {
    if (!highlights || highlights.length === 0) {
        return '<p>No highlights available</p>';
    }
    
    return highlights.map(highlight => 
        `<div class="insight-item">
            <strong>${highlight.type || 'Highlight'}:</strong> ${highlight.description || ''}
        </div>`
    ).join('');
}

function showError(message) {
    document.getElementById('error').textContent = message;
    document.getElementById('error').style.display = 'block';
}

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Find and activate the clicked tab button
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        if (tab.getAttribute('data-tab') === tabName) {
            tab.classList.add('active');
        }
    });
}

