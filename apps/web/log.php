<!-- BUDGOAPPV2/site/pages/log.php -->
<!-- CREATED BY José -->
<?php
require_once __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Connexion / Inscription</title>
        <meta name="description" content="Je créer mon cv en ligne 100% gratuit">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="css/style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <link rel="icon" type="image/x-icon" href="img/icon.ico">
    </head>
    <body>
        <?php
        include BASE_PATH . '/header.php';
        ?>
        <main>
            <div class="page-login">
                <div id="log_contener">
                    <?php if (isset($_GET['activated'])): ?>
                    <div class="flash-overlay" id="flashOverlay">
                        <div class="flash flash-<?=$_GET['activated']=='1'?'success':'error'?>">
                        <button class="flash-close" onclick="closeFlash()">✕</button>

                        <?php if ($_GET['activated'] == '1'): ?>
                            <h3>🎉 Compte activé</h3>
                            <p>Ton compte est maintenant actif.<br>Tu peux te connecter.</p>
                        <?php else: ?>
                            <h3>❌ Lien invalide</h3>
                            <p>Ce lien est invalide ou a expiré.</p>
                        <?php endif; ?>
                        </div>
                    </div>
                    <?php endif; ?>
                    <?php if (isset($_GET['registered'])): ?>
                    <div class="flash-overlay" id="flashOverlay">
                        <div class="flash flash-success">
                        <button class="flash-close" onclick="closeFlash()">✕</button>
                        <h3>✅ Compte créé</h3>
                        <p>
                            Félicitations, ton compte est créé.<br>
                            Regarde tes mails pour l’activer (pense aux spams).
                        </p>
                        </div>
                    </div>
                    <?php endif; ?>
                    <?php if (isset($_GET['regerr'])): ?>
                    <div class="flash-overlay" id="flashOverlay">
                        <div class="flash flash-error">
                        <button class="flash-close" onclick="closeFlash()">✕</button>
                        <h3>❌ Inscription échouée</h3>
                        <p><?= htmlspecialchars($_GET['regerr']) ?></p>
                        </div>
                    </div>
                    <?php endif; ?>
                    <!-- Onglets -->
                    <div class="tab-header">
                        <div class="tab" data-target="#connexionForm">Connexion</div>
                        <div class="tab active" data-target="#inscriptionForm">Inscription</div>
                    </div>
                    <div class="form_container">
                        <!-- Formulaire Connexion -->
                        <form id="connexionForm" action="connect_user.php" method="POST">
                            <div class="input-group">
                                <input type="text" name="login" required placeholder=" ">
                                <label>Email (ou pseudo)</label>
                            </div>
                            <div class="input-group">
                                <input type="password" name="password" required placeholder=" ">
                                <label>Mot de passe</label>
                            </div>
                            <div class="forgot-password">
                                <a href="reset_password.php">Mot de passe oublié ?</a>
                            </div>
                            <button type="submit" class="choix-btn">Se connecter</button>
                                                        <div class="oauth-divider"><span>ou se connecter avec</span></div>
                            <div class="oauth-buttons">
                            <a class="oauth-btn oauth-google" href="oauth_google_start.php">
                                <i class="fa-brands fa-google"></i>
                                Google
                            </a>
                            <a class="oauth-btn oauth-apple" href="oauth_apple_start.php">
                                <i class="fa-brands fa-apple"></i>
                                Apple
                            </a>
                            </div>
                            <div class="oauth-note">
                            En continuant, tu acceptes les CGU et la politique de confidentialité.
                            </div>
                        </form>
                        <!-- Formulaire Inscription -->
                        <form id="inscriptionForm">
                            <div class="input-group">
                                <span class="error-msg"></span>
                                <input type="text" id="username" name="username" required placeholder=" ">
                                <label>Pseudo</label>
                            </div>
                            <div class="input-group">
                                <span class="error-msg"></span>
                                <input type="email" id="email" name="email" required placeholder=" ">
                                <label>Email</label>
                            </div>
                            <div class="input-group">
                                <span class="error-msg"></span>
                                <input type="password" id="password" name="password" required placeholder=" ">
                                <label>Mot de passe</label>
                            </div>
                            <div class="input-group">
                                <span class="error-msg"></span>
                                <input type="password" id="password_confirm" name="password_confirm" required placeholder=" ">
                                <label>Confirmer le mot de passe</label>
                            </div>
                            <button type="submit" class="choix-btn" disabled>S'inscrire</button>
                            <div class="oauth-divider"><span>ou s’inscrire avec</span></div>
                            <div class="oauth-buttons">
                            <a class="oauth-btn oauth-google" href="oauth_google_start.php">
                                <i class="fa-brands fa-google"></i>
                                Google
                            </a>
                            <a class="oauth-btn oauth-apple" href="oauth_apple_start.php">
                                <i class="fa-brands fa-apple"></i>
                                Apple
                            </a>
                            </div>
                            <div class="oauth-note">
                            En continuant, tu acceptes les CGU et la politique de confidentialité.
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </main>
        <?php
        include BASE_PATH . '/footer.php';
        ?>
    </body>
    <script src="js/log.js"></script>
</html>