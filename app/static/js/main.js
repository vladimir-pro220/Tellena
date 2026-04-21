/* ================================================================
   main.js — THENELLA Ministries
   Extrait et adapté depuis index.html (Étape 21)

   Changements vs version statique originale :
   - Formulaire → fetch() vers /contact (POST JSON) au lieu de alert()
   - Affichage d'un message de succès/erreur dans #form-message
   - Langue courante envoyée dans le payload (champ "language")
   ================================================================ */


// ----------------------------------------------------------------
// 1. Sélecteurs DOM
// ----------------------------------------------------------------
const header          = document.getElementById('header');
const hamburger       = document.getElementById('hamburger');
const navLinks        = document.getElementById('nav-links');
const langEnBtn       = document.getElementById('lang-en');
const langFrBtn       = document.getElementById('lang-fr');
const sliderContainer = document.getElementById('slider-container');
const prevBtn         = document.getElementById('prev-btn');
const nextBtn         = document.getElementById('next-btn');
const bookingForm     = document.getElementById('booking-form');
const formMessage     = document.getElementById('form-message');


// ----------------------------------------------------------------
// 2. Langue courante (initialisée en anglais)
// ----------------------------------------------------------------
let currentLang = 'en';


// ----------------------------------------------------------------
// 3. Header — effet de défilement
// ----------------------------------------------------------------
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});


// ----------------------------------------------------------------
// 4. Navigation mobile — menu burger
// ----------------------------------------------------------------
hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    hamburger.innerHTML = navLinks.classList.contains('active')
        ? '<i class="fas fa-times"></i>'
        : '<i class="fas fa-bars"></i>';
});

// Fermer le menu mobile au clic sur un lien
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        hamburger.innerHTML = '<i class="fas fa-bars"></i>';
    });
});


// ----------------------------------------------------------------
// 5. Slider d'images
// ----------------------------------------------------------------
let currentSlide = 0;
const slides     = document.querySelectorAll('.slide');
const totalSlides = slides.length;

function updateSlider() {
    sliderContainer.style.transform = `translateX(-${currentSlide * 100}%)`;
}

nextBtn.addEventListener('click', () => {
    currentSlide = (currentSlide + 1) % totalSlides;
    updateSlider();
});

prevBtn.addEventListener('click', () => {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    updateSlider();
});

// Défilement automatique toutes les 5 secondes
setInterval(() => {
    currentSlide = (currentSlide + 1) % totalSlides;
    updateSlider();
}, 5000);


// ----------------------------------------------------------------
// 6. Sélecteur de langue (EN / FR)
// ----------------------------------------------------------------
function switchLanguage(lang) {
    currentLang = lang;

    // Mise à jour de l'état actif des boutons
    if (lang === 'en') {
        langEnBtn.classList.add('active');
        langFrBtn.classList.remove('active');
    } else {
        langFrBtn.classList.add('active');
        langEnBtn.classList.remove('active');
    }

    // Mise à jour de tous les éléments portant data-lang-en / data-lang-fr
    document.querySelectorAll('[data-lang-en]').forEach(element => {
        const text = element.getAttribute(`data-lang-${lang}`);
        if (!text) return;

        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            element.placeholder = text;   // utilise placeholder pour ne pas écraser la saisie
        } else {
            element.textContent = text;
        }
    });

    // Mise à jour des options du select
    document.querySelectorAll('option[data-lang-en]').forEach(option => {
        const text = option.getAttribute(`data-lang-${lang}`);
        if (text) option.textContent = text;
    });
}

langEnBtn.addEventListener('click', () => switchLanguage('en'));
langFrBtn.addEventListener('click', () => switchLanguage('fr'));


// ----------------------------------------------------------------
// 7. Soumission du formulaire de réservation → POST /contact
// ----------------------------------------------------------------
if (bookingForm) {
    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Récupération des valeurs
        const name      = document.getElementById('name').value.trim();
        const email     = document.getElementById('email').value.trim();
        const phone     = document.getElementById('phone').value.trim();
        const eventType = document.getElementById('event-type').value;
        const message   = document.getElementById('message').value.trim();

        // Désactiver le bouton pendant l'envoi
        const submitBtn = bookingForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = currentLang === 'en' ? 'Sending...' : 'Envoi en cours...';

        try {
            const response = await fetch('/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name,
                    email,
                    phone,
                    event_type: eventType,
                    message,
                    language: currentLang
                })
            });

            const data = await response.json();

            // Affichage du message de retour
            formMessage.className = `form-message ${data.success ? 'success' : 'error'}`;
            formMessage.textContent = data.message;
            formMessage.style.display = 'block';

            if (data.success) {
                // Réinitialisation du formulaire en cas de succès
                bookingForm.reset();
                switchLanguage(currentLang); // remet les labels dans la bonne langue
            }

        } catch (err) {
            // Erreur réseau ou serveur inattendue
            formMessage.className = 'form-message error';
            formMessage.textContent = currentLang === 'en'
                ? 'A network error occurred. Please try again.'
                : 'Une erreur réseau s\'est produite. Veuillez réessayer.';
            formMessage.style.display = 'block';
        } finally {
            // Réactiver le bouton dans tous les cas
            submitBtn.disabled = false;
            submitBtn.textContent = currentLang === 'en'
                ? 'Send Booking Request'
                : 'Envoyer la Demande de Réservation';

            // Masquer le message après 6 secondes
            setTimeout(() => {
                formMessage.style.display = 'none';
            }, 6000);
        }
    });
}


// ----------------------------------------------------------------
// 8. Smooth scrolling pour les ancres internes
// ----------------------------------------------------------------
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});


// ----------------------------------------------------------------
// 9. Initialisation au chargement de la page
// ----------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    switchLanguage('en');
});