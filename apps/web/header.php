<!-- /BUDGOAPPV2/site/pages/header.php -->
<!-- CREATED BY José -->
<header>
    <div class="logo">
        <a href="/">
            <img src="img/logo_site.png" alt="BudgoApp Logo" class="logo-img">
            BudgoApp.com
        </a>
    </div>
    <div class="menu-toggle" id="menu-toggle">☰</div>
        <nav id="nav-menu">
                <a href="log.php" class="go-login">Connexion / Inscription</a>
        </nav>
</header>
<script>
document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.getElementById('nav-menu');

    if(menuToggle){
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('show');
        });
    }
});
</script>