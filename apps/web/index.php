<!--index.php -->
<!-- CREATED BY José -->
<?php
require_once __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="fr">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BudgoApp - Gestionnaire Budget</title>
    <meta name="description" content="BudgoApp vous aide è gérer votre budget, suivre vos dépense et mieux economiser grâce à un système clair et moderne.">
    <link rel="stylesheet" href="css/style.css">
    <link rel="shortcut icon" href="img/icon.ico" type="image/x-icon">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="apple-touch-icon" href="img/logo_icon_site.ico">
    </head>
    <body>
        <?php
        include BASE_PATH . '/header.php';
        ?>
        <main>
            <section class="hero">
            <h1>Gérez vos finances facilement</h1>
            <p>Saisissez vos revenus, vos dépenses, créer des enveloppes de projets, et laissez BudgoAppIA répartir automatiquement votre budget</p>
            <a href="#" class="btn">Commencer</a>
            </section>
            <section class="features">
            <div class="feature">
                <h3>Projets / Enveloppes</h3>
                <p>Créez vos projets et répartissez votre budget facilement</p>
            </div>
            <div class="feature">
                <h3>Suivi clair</h3>
                <p>Visualisez vos dépenses et votre solde global en un coup d'œil</p>
            </div>
            <div class="feature">
                <h3>Simple et rapide</h3>
                <p>Ajoutez vos transactions en quelques secondes et restez à jour</p>
            </div>
            </section>
        </main>
        <?php
        include BASE_PATH . '/footer.php';
        ?>
    </body>
</html>