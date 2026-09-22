document.getElementById('send').addEventListener('click', async () => {
  const prompt = document.getElementById('prompt').value;
  const max_tokens = parseInt(document.getElementById('max_tokens').value || '128');
  const temperature = parseFloat(document.getElementById('temperature').value || '0.7');
  const out = document.getElementById('out');
  out.textContent = 'Thinking...';

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, max_tokens, temperature })
    });
    const data = await res.json();
    if (data.error) {
      out.textContent = 'Error: ' + data.error;
    } else {
      out.textContent = data.text || JSON.stringify(data);
    }
  } catch (err) {
    out.textContent = 'Request failed: ' + err;
  }
});
