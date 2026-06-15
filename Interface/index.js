async function submitCode() {
    const payload = {
        challenge_id: parseInt(document.getElementById('challengeId').value),
        user_id: parseInt(document.getElementById('userId').value),
        code: document.getElementById('code').value
    };

    const outputDisplay = document.getElementById('output');
    const resultContainer = document.getElementById('resultContainer');
    const runBtn = document.getElementById('runBtn');

    resultContainer.style.display = "block";
    outputDisplay.className = "output-box loading";
    outputDisplay.textContent = "Executing in secure sandbox";
    runBtn.disabled = true;

    try {
        const res = await fetch('http://127.0.0.1:8000/submit/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok) {
            const captured = data.is_correct;
            const status = captured ? "✓ FLAG CAPTURED\n" : "✗ FAILED\n";
            outputDisplay.textContent = status + "------------------\n" + data.execution_output;
            outputDisplay.className = "output-box " + (captured ? "success" : "error-box");
        } else {
            outputDisplay.textContent = "Server Error: " + data.detail;
            outputDisplay.className = "output-box error-box";
        }
    } catch (error) {
        outputDisplay.textContent = "Submission failed. Make sure the Uvicorn server is running.";
        outputDisplay.className = "output-box error-box";
        console.error(error);
    } finally {
        runBtn.disabled = false;
    }
}

// Ctrl/Cmd + Enter to execute
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        submitCode();
    }
});
