var RAW_LICENSE = 'https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/LICENSE';

async function loadLicense() {
  var skeleton = document.getElementById('docSkeleton');
  var body = document.getElementById('docBody');

  try {
    var res = await fetch(RAW_LICENSE);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    var text = await res.text();

    // Render plain text inside a pre block for formatting preservation
    body.innerHTML = '<pre style="background:transparent;border:none;padding:0;overflow-x:auto;"><code>' + 
      text.replace(/</g, '&lt;').replace(/>/g, '&gt;') + 
      '</code></pre>';
      
    if (skeleton) skeleton.remove();
    body.hidden = false;

  } catch (e) {
    if (skeleton) skeleton.remove();
    body.innerHTML = '<div class="gh-error-state"><i class="bi bi-exclamation-triangle"></i><p>Failed to load License. Please check GitHub directly.</p><a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/blob/master/LICENSE" target="_blank" rel="noopener" class="btn gh-fallback-btn">View on GitHub</a></div>';
    body.hidden = false;
  }
}

loadLicense();
