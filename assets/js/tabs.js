(function() {
  function initTabs() {
    var tabs = document.querySelectorAll('.term-tab');
    var contents = document.querySelectorAll('.term-content');
    if (tabs.length === 0) return;
    
    tabs.forEach(function(tab) {
      tab.addEventListener('click', function(e) {
        e.preventDefault();
        tabs.forEach(function(t) { t.classList.remove('active'); });
        contents.forEach(function(c) { c.classList.remove('active'); });
        
        tab.classList.add('active');
        var termId = tab.getAttribute('data-term');
        var content = document.getElementById('term-' + termId);
        if (content) {
          content.classList.add('active');
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTabs);
  } else {
    initTabs();
  }
})();
