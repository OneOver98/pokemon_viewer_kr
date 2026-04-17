document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const searchBtn = document.getElementById('searchBtn');
  const suggestionsBox = document.getElementById('suggestionsBox');
  const teamContainer = document.getElementById('teamContainer');
  const playerNameEl = document.getElementById('playerName');
  const copyBtn = document.getElementById('copyBtn');

  let trainersData = [];
  let currentTrainer = null;

  fetch('data.json')
    .then(res => res.json())
    .then(data => trainersData = data)
    .catch(err => console.error("Error loading data:", err));

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (!query) {
      suggestionsBox.classList.remove('active');
      return;
    }
    const matches = trainersData.filter(t => 
      t.trainer_name.toLowerCase().includes(query) || 
      t.gamertag.toLowerCase().includes(query)
    ).slice(0, 5);

    if (matches.length > 0) {
      suggestionsBox.innerHTML = matches.map(m => {
        const name = m.trainer_name || m.gamertag;
        return `<div class="suggestion-item" data-id="${name}">${name}</div>`;
      }).join('');
      suggestionsBox.classList.add('active');
    } else {
      suggestionsBox.classList.remove('active');
    }
  });

  suggestionsBox.addEventListener('click', (e) => {
    const item = e.target.closest('.suggestion-item');
    if (item) {
      const selectedId = item.getAttribute('data-id');
      searchInput.value = selectedId;
      suggestionsBox.classList.remove('active');
      searchTrainer(selectedId);
    }
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container-wrap')) {
      suggestionsBox.classList.remove('active');
    }
  });

  searchBtn.addEventListener('click', () => searchTrainer(searchInput.value.trim()));
  searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      suggestionsBox.classList.remove('active');
      searchTrainer(searchInput.value.trim());
    }
  });

  function searchTrainer(query) {
    if (!query) return;
    const lowerQuery = query.toLowerCase();
    const trainer = trainersData.find(t => 
      t.trainer_name.toLowerCase() === lowerQuery || 
      t.gamertag.toLowerCase() === lowerQuery
    );
    if (trainer) displayTrainer(trainer);
    else {
      teamContainer.innerHTML = '<p style="padding:20px; color:red;">Trainer not found.</p>';
      playerNameEl.style.display = 'none';
      currentTrainer = null;
    }
  }

  function displayTrainer(trainer) {
    currentTrainer = trainer;
    playerNameEl.textContent = trainer.trainer_name || trainer.gamertag;
    playerNameEl.style.display = 'block';
    teamContainer.innerHTML = '';

    trainer.pokemon.forEach(p => {
      const card = document.createElement('div');
      card.className = 'poke single';

      // Type badges DOM
      const typesHtml = p.types.filter(t => t && t !== 'none').map(t => `<div class="type ${t}">${t}</div>`).join('');
      
      const fType = p.fast_type && p.fast_type !== 'none' ? p.fast_type : 'normal';
      const fName = p.fast_move ? p.fast_move.replace(/_/g, ' ') : '-';
      
      const c1Type = p.charge1_type && p.charge1_type !== 'none' ? p.charge1_type : 'normal';
      const c1Name = p.charge1 ? p.charge1.replace(/_/g, ' ') : '-';
      
      const c2Type = p.charge2_type && p.charge2_type !== 'none' ? p.charge2_type : 'normal';
      const c2Name = p.charge2 ? p.charge2.replace(/_/g, ' ') : '-';

      card.innerHTML = `
        <h3 class="base-name">${p.eng_name || 'Unknown'}${p.is_shadow ? ' <span style="color:#b763cf; font-size:14px; vertical-align:middle; text-shadow:none; font-weight:800;">(SHADOW)</span>' : ''}</h3>
        <div class="poke-stats">
          <h3 class="cp">cp <span class="stat">${p.cp}</span> &nbsp;&nbsp;&nbsp; hp <span class="stat">${p.hp || '-'}</span></h3>
          <div class="types">
            ${typesHtml}
          </div>
          
          <div class="move-select-container">
            <h3 class="section-title">Fast Move</h3>
            <div class="move-select fast">
              <div class="type ${fType}">${fType}</div>
              <div class="name">${fName}</div>
            </div>
            
            <h3 class="section-title">Charged Moves</h3>
            <div class="move-select charged">
              <div class="type ${c1Type}">${c1Type}</div>
              <div class="name">${c1Name}</div>
            </div>
            <div class="move-select charged" style="${p.charge2 ? '' : 'opacity:0.3;'}">
              <div class="type ${c2Type}">${c2Type}</div>
              <div class="name">${c2Name}</div>
            </div>
          </div>
        </div>
      `;
      teamContainer.appendChild(card);
    });
  }

  copyBtn.addEventListener('click', () => {
    if (!currentTrainer) return;
    const lines = currentTrainer.pokemon.map(p => p.export_str);
    const exportData = lines.join('\n');
    navigator.clipboard.writeText(exportData)
      .then(() => alert("Copied export string to clipboard!"))
      .catch(err => console.error("Could not copy text: ", err));
  });
});
