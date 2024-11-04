let lastAnalyzedJob = null;
let currentStep = 1;
let jobAnalysis = null;
let optimizedResume = null;

function showProcessStarted(buttonId, loadingText) {
    const button = document.getElementById(buttonId);
    button.disabled = true;
    button.innerHTML = `
        <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        ${loadingText}
    `;
}

function resetButton(buttonId, originalText) {
    const button = document.getElementById(buttonId);
    button.disabled = false;
    button.innerHTML = originalText;
}

async function addApplication(event) {
    event.preventDefault();
    
    const data = {
        company: document.getElementById('company').value,
        position: document.getElementById('position').value,
        job_link: document.getElementById('jobLink').value || null,
        priority: parseInt(document.getElementById('priority').value)
    };

    try {
        const response = await fetch('/applications/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        if (result.status === "success") {
            alert('Application added successfully!');
            document.getElementById('applicationForm').reset();
            loadApplications();
        } else {
            alert('Error adding application: ' + result.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding application: ' + error.message);
    }
}

async function analyzeJob() {
    const jobDescription = document.getElementById('jobDescription').value;
    const button = document.getElementById('analyzeButton');
    const resultBox = document.getElementById('analysisResult');
    const workingIndicator = resultBox.querySelector('.agent-working');
    const resultContent = resultBox.querySelector('.agent-result');
    
    if (!jobDescription.trim()) {
        alert('Please enter a job description');
        return;
    }
    
    try {
        // Show loading state
        button.disabled = true;
        button.classList.add('loading');
        button.querySelector('.button-loader').classList.remove('hidden');
        button.querySelector('.button-text').classList.add('hidden');
        
        resultBox.style.display = 'block';
        workingIndicator.classList.remove('hidden');
        resultContent.classList.add('hidden');
        
        console.log('Sending job description for analysis:', jobDescription.substring(0, 100) + '...');
        
        const response = await fetch('/analyze-job/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                job_description: jobDescription 
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }
        
        const data = await response.json();
        console.log('Received analysis:', data);
        
        // Store for later use
        jobAnalysis = data.analysis;
        lastAnalyzedJob = jobDescription;
        
        // Format and display the analysis
        workingIndicator.classList.add('hidden');
        resultContent.classList.remove('hidden');
        resultContent.innerHTML = formatAnalysis(data.analysis);
        
        // Enable next step
        document.getElementById('optimizeButton').disabled = false;
        currentStep = 2;
        updateAgentFlow(currentStep);
        
    } catch (error) {
        console.error('Error:', error);
        resultContent.innerHTML = `
            <div class="feedback-message error">
                <i class="fas fa-exclamation-circle"></i>
                Error analyzing job: ${error.message}
            </div>
        `;
    } finally {
        // Reset button state
        button.disabled = false;
        button.classList.remove('loading');
        button.querySelector('.button-loader').classList.add('hidden');
        button.querySelector('.button-text').classList.remove('hidden');
    }
}

function formatAnalysis(analysis) {
    // If analysis is a string, parse it if it looks like JSON
    let analysisData = analysis;
    if (typeof analysis === 'string') {
        try {
            analysisData = JSON.parse(analysis);
        } catch (e) {
            // If it's not JSON, keep it as a string
            analysisData = analysis;
        }
    }

    // If it's an object, format it nicely
    if (typeof analysisData === 'object') {
        return `
            <div class="analysis-result">
                <h3>Job Analysis Results</h3>
                ${Object.entries(analysisData).map(([key, value]) => `
                    <div class="analysis-section">
                        <h4>${key.replace(/_/g, ' ').toUpperCase()}</h4>
                        ${formatValue(value)}
                    </div>
                `).join('')}
            </div>
        `;
    }

    // If it's a string, format with markdown-style parsing
    return `
        <div class="analysis-result">
            ${analysisData
                .replace(/### (.*?)\n/g, '<h3>$1</h3>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .split('\n\n')
                .map(para => {
                    if (para.startsWith('- ')) {
                        const items = para.split('\n- ').filter(item => item);
                        return `<ul>${items.map(item => `<li>${item}</li>`).join('')}</ul>`;
                    }
                    return `<p>${para}</p>`;
                })
                .join('')}
        </div>
    `;
}

function formatValue(value) {
    if (Array.isArray(value)) {
        return `<ul>${value.map(item => `<li>${item}</li>`).join('')}</ul>`;
    } else if (typeof value === 'object') {
        return `<div class="nested-object">
            ${Object.entries(value).map(([k, v]) => `
                <div class="object-item">
                    <strong>${k.replace(/_/g, ' ')}:</strong> 
                    ${formatValue(v)}
                </div>
            `).join('')}
        </div>`;
    }
    return `<span>${value}</span>`;
}

async function optimizeResume() {
    const resume = document.getElementById('resume').value;
    const resultBox = document.getElementById('optimizationResult');
    const workingIndicator = resultBox.querySelector('.agent-working');
    const resultContent = resultBox.querySelector('.agent-result');
    
    if (!resume.trim()) {
        alert('Please enter your resume');
        return;
    }
    
    if (!lastAnalyzedJob) {
        alert('Please analyze a job description first');
        return;
    }
    
    try {
        // Show working state
        showProcessStarted('optimizeButton', 'Resume Builder Agent Optimizing...');
        resultBox.style.display = 'block';
        workingIndicator.classList.remove('hidden');
        resultContent.classList.add('hidden');
        
        const response = await fetch('/optimize-resume/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                resume: resume,
                job_requirements: lastAnalyzedJob
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to optimize resume');
        }
        
        const data = await response.json();
        
        // Format and display the result
        const formattedResume = formatOptimizedResume(data.optimized_resume);
        workingIndicator.classList.add('hidden');
        resultContent.classList.remove('hidden');
        resultContent.innerHTML = formattedResume;
        
        // Enable next step
        document.getElementById('prepButton').disabled = false;
        currentStep = 3;
        updateAgentFlow(currentStep);
        
    } catch (error) {
        console.error('Error:', error);
        resultContent.innerHTML = `<div class="error">Error optimizing resume: ${error.message}</div>`;
    } finally {
        resetButton('optimizeButton', 'Optimize Resume');
    }
}

function formatOptimizedResume(resume) {
    return `
        <div class="optimization-result">
            <h2>Optimized Resume</h2>
            <div class="formatted-content">
                ${resume
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/### (.*?)\n/g, '<h3>$1</h3>')
                    .replace(/\[(.*?)\]/g, '<span class="highlight">$1</span>')
                    .split('\n\n')
                    .map(para => {
                        if (para.startsWith('- ')) {
                            const items = para.split('\n- ').filter(item => item);
                            return `<ul>${items.map(item => `<li>${item}</li>`).join('')}</ul>`;
                        }
                        return `<p>${para}</p>`;
                    })
                    .join('')}
            </div>
        </div>
    `;
}

async function loadApplications() {
    try {
        const response = await fetch('/applications/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const applicationsList = document.getElementById('applicationsList');
        applicationsList.innerHTML = '';
        
        if (!data.applications || data.applications.length === 0) {
            applicationsList.innerHTML = '<p>No applications found</p>';
            return;
        }
        
        data.applications.forEach(app => {
            applicationsList.innerHTML += `
                <div class="application-card">
                    <h3>${app.company || 'Unknown Company'}</h3>
                    <p>Position: ${app.position || 'Unknown Position'}</p>
                    <p>Status: ${app.status || 'Unknown Status'}</p>
                    <p>Priority: ${app.priority || 'Unknown Priority'}</p>
                    ${app.job_link ? `<p><a href="${app.job_link}" target="_blank">Job Link</a></p>` : ''}
                </div>
            `;
        });
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('applicationsList').innerHTML = 
            `<p>Error loading applications: ${error.message}</p>`;
    }
}

function updateSectionVisibility() {
    document.querySelectorAll('.section').forEach((section, index) => {
        if (index + 1 === currentStep) {
            section.classList.add('active');
            section.style.opacity = '1';
            section.style.pointerEvents = 'all';
        } else {
            section.classList.remove('active');
            section.style.opacity = '0.7';
            section.style.pointerEvents = 'none';
        }
    });
}

function updateAgentFlow(step) {
    currentStep = step;
    
    // Reset all steps
    document.querySelectorAll('.agent-step').forEach(el => {
        el.classList.remove('active', 'completed');
    });
    
    // Mark completed and active steps
    for (let i = 1; i <= 4; i++) {
        const stepEl = document.getElementById(`step${i}`);
        if (i < step) {
            stepEl.classList.add('completed');
        } else if (i === step) {
            stepEl.classList.add('active');
        }
    }
    
    updateSectionVisibility();
}

// Add event listeners when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('applicationForm');
    if (form) {
        form.addEventListener('submit', addApplication);
    }
    
    // Enable first section by default
    updateAgentFlow(1);
    const jobAnalysisSection = document.getElementById('jobAnalysisSection');
    if (jobAnalysisSection) {
        jobAnalysisSection.style.opacity = '1';
        jobAnalysisSection.style.pointerEvents = 'all';
    }
    
    // Make sure the job description textarea is enabled
    const jobDescription = document.getElementById('jobDescription');
    if (jobDescription) {
        jobDescription.disabled = false;
    }
    
    loadApplications();
}); 