document.addEventListener('DOMContentLoaded', () => {
    // Menu Toggle (Hamburguer)
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
  
    if (navToggle && navMenu) {
      navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
      });
    }
  
    // Theme Toggle (Dark/Light Mode)
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
  
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      html.setAttribute('data-theme', savedTheme);
      themeToggle.textContent = savedTheme === 'dark' ? '☀' : '☾';
    }
  
    if (themeToggle) {
      themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        themeToggle.textContent = newTheme === 'dark' ? '☀' : '☾';
      });
    }
  
    // Filtro de Busca em Tempo Real
    const searchInput = document.getElementById('search-input');
    const postsContainer = document.getElementById('posts-container');
  
    if (searchInput && postsContainer) {
      searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        const posts = postsContainer.querySelectorAll('.post-card');
        
        posts.forEach(post => {
          const title = post.querySelector('.post-card__title').textContent.toLowerCase();
          const excerpt = post.querySelector('.post-card__excerpt').textContent.toLowerCase();
          
          if (title.includes(query) || excerpt.includes(query)) {
            post.style.display = '';
          } else {
            post.style.display = 'none';
          }
        });
      });
    }
  });
  