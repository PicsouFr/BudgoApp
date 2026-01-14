<?php
require_once __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="fr">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>contact</title>
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
        <main class="contact-container">
            <h1>Contact</h1>
            <p class="contact-intro">
                Une question, un bug, une idée d’amélioration. Envoie un message.
            </p>

            <?php if (isset($_GET["sent"]) && $_GET["sent"] === "1"): ?>
                <div class="contact-alert success">Message envoyé. Merci.</div>
            <?php elseif (isset($_GET["err"])): ?>
                <div class="contact-alert error">Impossible d’envoyer le message. Réessaie.</div>
            <?php endif; ?>

            <form class="contact-form" method="post" action="contact_send.php">
                <label for="name">Nom</label>
                <input id="name" name="name" type="text" autocomplete="name" required>

                <label for="email">Email</label>
                <input id="email" name="email" type="email" autocomplete="email" required>

                <label for="subject">Sujet</label>
                <input id="subject" name="subject" type="text" required>

                <label for="message">Message</label>
                <textarea id="message" name="message" rows="7" required></textarea>

                <button type="submit" class="contact-btn">Envoyer</button>

                <p class="contact-alt">
                Tu peux aussi écrire à :
                <a href="mailto:contact@budgoapp.com">contact@budgoapp.com</a>
                </p>
            </form>
        </main>
        <?php
        include BASE_PATH . '/footer.php';
        ?>
    </body>
</html>