let lastAnalyzedJob = null;

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
    const resultBox = document.getElementById('analysisResult');
    
    if (!jobDescription.trim()) {
        alert('Please enter a job description');
        return;
    }
    
    resultBox.style.display = 'block';
    resultBox.innerHTML = '<div class="loading">Analyzing...</div>';
    
    try {
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
            const error = await response.json();
            throw new Error(error.detail || 'Failed to analyze job description');
        }
        
        const data = await response.json();
        lastAnalyzedJob = jobDescription;
        
        const formattedAnalysis = data.analysis
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/### (.*?)\n/g, '<h3>$1</h3>')
            .split('\n\n')
            .map(para => {
                if (para.startsWith('- ')) {
                    const items = para.split('\n- ').filter(item => item);
                    return `<ul>${items.map(item => `<li>${item}</li>`).join('')}</ul>`;
                }
                return `<p>${para}</p>`;
            })
            .join('');

        resultBox.innerHTML = `
            <div class="analysis-result">
                ${formattedAnalysis}
            </div>
        `;
    } catch (error) {
        console.error('Error:', error);
        resultBox.innerHTML = `<div class="error">Error analyzing job description: ${error.message}</div>`;
    }
}

async function optimizeResume() {
    const resume = document.getElementById('resume').value;
    const resultBox = document.getElementById('optimizationResult');
    
    if (!resume.trim()) {
        alert('Please enter your resume');
        return;
    }
    
    if (!lastAnalyzedJob) {
        alert('Please analyze a job description first');
        return;
    }
    
    resultBox.style.display = 'block';
    resultBox.innerHTML = '<div class="loading">Optimizing resume...</div>';
    
    try {
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
        
        // Format the optimized resume similar to job analysis
        const formattedResume = data.optimized_resume
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold text
            .replace(/### (.*?)\n/g, '<h3>$1</h3>')           // Headers
            .replace(/\[(.*?)\]/g, '<span class="highlight">$1</span>') // Highlights
            .split('\n\n')                                     // Split paragraphs
            .map(para => {
                if (para.startsWith('- ')) {
                    // Convert bullet points to list items
                    const items = para.split('\n- ').filter(item => item);
                    return `<ul>${items.map(item => `<li>${item}</li>`).join('')}</ul>`;
                }
                return `<p>${para}</p>`;
            })
            .join('');

        resultBox.innerHTML = `
            <div class="optimization-result">
                <h2>Optimized Resume</h2>
                <div class="formatted-content">
                    ${formattedResume}
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error:', error);
        resultBox.innerHTML = `<div class="error">Error optimizing resume: ${error.message}</div>`;
    }
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

// Add event listeners when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('applicationForm');
    if (form) {
        form.addEventListener('submit', addApplication);
    }
    loadApplications();
}); 