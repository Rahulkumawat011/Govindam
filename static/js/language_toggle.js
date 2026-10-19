/**
 * Govindam Enterprises - English / Hindi Dual Language Toggle System
 * Switches entire website between English and Hindi (हिंदी) with persistence in localStorage and cookies.
 */

(function () {
    'use strict';

    // Helper to get cookie value
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    // Helper to set cookie for current path and domain
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        const host = window.location.hostname;
        document.cookie = `${name}=${value}${expires}; path=/; domain=${host}`;
        document.cookie = `${name}=${value}${expires}; path=/;`;
    }

    // Update Language Toggle Button UI Labels across the page
    window.updateLangButtonUI = function (lang) {
        const langLabels = document.querySelectorAll('.lang-label');
        langLabels.forEach(el => {
            if (lang === 'hi') {
                el.innerText = 'English';
            } else {
                el.innerText = 'हिंदी';
            }
        });
    };

    // Toggle Language Function
    window.toggleLanguage = function () {
        const currentLang = localStorage.getItem('site_language') || 'en';
        const targetLang = currentLang === 'en' ? 'hi' : 'en';
        
        localStorage.setItem('site_language', targetLang);
        updateLangButtonUI(targetLang);

        if (targetLang === 'hi') {
            setCookie('googtrans', '/en/hi', 30);
        } else {
            setCookie('googtrans', '/en/en', 30);
        }

        // Try triggering Google Translate select combo if loaded
        const combo = document.querySelector('.goog-te-combo');
        if (combo) {
            combo.value = targetLang;
            combo.dispatchEvent(new Event('change'));
        }
        
        // Reload page to apply clean translation state
        window.location.reload();
    };

    // Initialize Language settings on DOM load
    document.addEventListener('DOMContentLoaded', function () {
        const savedLang = localStorage.getItem('site_language') || 'en';
        
        // Sync cookie if out of sync
        if (savedLang === 'hi') {
            const currentCookie = getCookie('googtrans');
            if (!currentCookie || !currentCookie.includes('/hi')) {
                setCookie('googtrans', '/en/hi', 30);
            }
        }
        
        updateLangButtonUI(savedLang);
    });

    // Google Translate Callback function
    window.googleTranslateElementInit = function () {
        new google.translate.TranslateElement({
            pageLanguage: 'en',
            includedLanguages: 'en,hi',
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false
        }, 'google_translate_element');
    };

})();
