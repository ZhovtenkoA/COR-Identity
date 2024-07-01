

function setLanguage(language) {
    document.querySelectorAll("[data-translate]").forEach(function(element) {
        const key = element.getAttribute("data-translate");
        element.innerText = translations[language][key];
    });

    // Установка выбранного языка в выпадающем списке
    const langSelect = document.getElementById('lang-select');
    if (langSelect) {
        langSelect.value = language;
    }

    // Сохранение выбранного языка в localStorage
    localStorage.setItem('selectedLanguage', language);
}

// Функция для переключения языков
function switchLanguage(language) {
    setLanguage(language);
}

// Detect browser language or set default to 'ru'
const userLang = navigator.language || navigator.userLanguage;
const defaultLang = localStorage.getItem('selectedLanguage') || 
                   (userLang.startsWith('ru') ? 'ru' : 
                   userLang.startsWith('en') ? 'en' : 
                   userLang.startsWith('zh') ? 'zh' : 'uk');

document.addEventListener('DOMContentLoaded', function() {
    // Set initial language
    setLanguage(defaultLang);
});

const translations = {
    en: {
        title: "Authorization",
        "email-label": "Email:",
        "password-label": "Password:",
        "login-button": "Login",
        "login-button-google": "Login with Google",
        "login-button-facebook": "Login with Facebook",
        "registration": "Registration",
        "registration-button": "Register",
        "forgot-password-button": "Forgot password?",
        "message-ok": "Login successful",
        "message-error": "An error occurred, please try again",
        "confirmation-message": "Verification code sent to your email",
        "send-code-again": "Send code again",
        "invalid-code": "Invalid code, please try again",
        "password-mismatch": "Passwords do not match",
        "password-requirements": "Password must be between 8 and 15 characters",
        "signup-title": "Sign Up",
        "name-label": "Name:",
        "surname-label": "Surname:",
        "confirm-password-label": "Confirm Password:",
        "signup-button": "Sign Up",
    },
    ru: {
        title: "Авторизация",
        "email-label": "Электронная почта:",
        "password-label": "Пароль:",
        "login-button": "Войти",
        "login-button-google": "Войти через Google",
        "login-button-facebook": "Войти через Facebook",
        "registration": "Регистрация",
        "registration-button": "Регистрация",
        "forgot-password-button": "Забыли пароль?",
        "message-ok": "Успешный вход",
        "message-error": "Произошла ошибка, пожалуйста, попробуйте снова",
        "confirmation-message": "Код подтверждения отправлен на вашу почту",
        "send-code-again": "Отправить код снова",
        "invalid-code": "Неверный код, пожалуйста, попробуйте снова",
        "password-mismatch": "Пароли не совпадают",
        "password-requirements": "Пароль должен быть от 8 до 15 символов",
        "signup-title": "Регистрация",
        "name-label": "Имя:",
        "surname-label": "Фамилия:",
        "confirm-password-label": "Подтвердите пароль:",
        "signup-button": "Зарегистрироваться",
    },
    zh: {
        title: "授权",
        "email-label": "电子邮件:",
        "password-label": "密码:",
        "login-button": "登录",
        "login-button-google": "通过 Google 登录",
        "login-button-facebook": "通过 Facebook 登录",
        "registration": "注册",
        "registration-button": "注册",
        "forgot-password-button": "忘记密码?",
        "message-ok": "登录成功",
        "message-error": "发生错误，请重试",
        "confirmation-message": "验证码已发送到您的电子邮件",
        "send-code-again": "再次发送验证码",
        "invalid-code": "验证码无效，请重试",
        "password-mismatch": "密码不匹配",
        "password-requirements": "密码必须是8到15个字符",
        "signup-title": "注册",
        "name-label": "名字:",
        "surname-label": "姓氏:",
        "confirm-password-label": "确认密码:",
        "signup-button": "注册",
    },
    uk: {
        title: "Авторизація",
        "email-label": "Електронна пошта:",
        "password-label": "Пароль:",
        "login-button": "Увійти",
        "login-button-google": "Увійти через Google",
        "login-button-facebook": "Увійти через Facebook",
        "registration": "Реєстрація",
        "registration-button": "Реєстрація",
        "forgot-password-button": "Забули пароль?",
        "message-ok": "Успішний вхід",
        "message-error": "Виникла помилка, будь ласка, спробуйте ще раз",
        "confirmation-message": "Код підтвердження надіслано на вашу пошту",
        "send-code-again": "Надіслати код знову",
        "invalid-code": "Невірний код, будь ласка, спробуйте ще раз",
        "password-mismatch": "Паролі не збігаються",
        "password-requirements": "Пароль має бути від 8 до 15 символів",
        "signup-title": "Реєстрація",
        "name-label": "Ім'я:",
        "surname-label": "Прізвище:",
        "confirm-password-label": "Підтвердьте пароль:",
        "signup-button": "Зареєструватися",
    }
};


/*


const translations = {
    en: {
        title: "Authorization",
        "email-label": "Email:",
        "password-label": "Password:",
        "login-button": "Login",
        "login-button-google": "Login with Google",
        "login-button-facebook": "Login with Facebook",
        "registration": "Registration",
        "registration-button": "Register",
        "forgot-password-button": "Forgot password?",
        "message-ok": "Login successful",
        "message-error": "An error occurred, please try again",
        "confirmation-message": "Verification code sent to your email",
        "send-code-again": "Send code again",
        "invalid-code": "Invalid code, please try again",
        "password-mismatch": "Passwords do not match",
        "password-requirements": "Password must be between 8 and 15 characters",
        "signup-title": "Sign Up",
        "name-label": "Name:",
        "surname-label": "Surname:",
        "confirm-password-label": "Confirm Password:",
        "signup-button": "Sign Up",
    },
    ru: {
        title: "Авторизация",
        "email-label": "Электронная почта:",
        "password-label": "Пароль:",
        "login-button": "Войти",
        "login-button-google": "Войти через Google",
        "login-button-facebook": "Войти через Facebook",
        "registration": "Регистрация",
        "registration-button": "Регистрация",
        "forgot-password-button": "Забыли пароль?",
        "message-ok": "Успешный вход",
        "message-error": "Произошла ошибка, пожалуйста, попробуйте снова",
        "confirmation-message": "Код подтверждения отправлен на вашу почту",
        "send-code-again": "Отправить код снова",
        "invalid-code": "Неверный код, пожалуйста, попробуйте снова",
        "password-mismatch": "Пароли не совпадают",
        "password-requirements": "Пароль должен быть от 8 до 15 символов",
        "signup-title": "Регистрация",
        "name-label": "Имя:",
        "surname-label": "Фамилия:",
        "confirm-password-label": "Подтвердите пароль:",
        "signup-button": "Зарегистрироваться",
    },
    zh: {
        title: "授权",
        "email-label": "电子邮件:",
        "password-label": "密码:",
        "login-button": "登录",
        "login-button-google": "通过 Google 登录",
        "login-button-facebook": "通过 Facebook 登录",
        "registration": "注册",
        "registration-button": "注册",
        "forgot-password-button": "忘记密码?",
        "message-ok": "登录成功",
        "message-error": "发生错误，请重试",
        "confirmation-message": "验证码已发送到您的电子邮件",
        "send-code-again": "再次发送验证码",
        "invalid-code": "验证码无效，请重试",
        "password-mismatch": "密码不匹配",
        "password-requirements": "密码必须是8到15个字符",
        "signup-title": "注册",
        "name-label": "名字:",
        "surname-label": "姓氏:",
        "confirm-password-label": "确认密码:",
        "signup-button": "注册",
    },
    uk: {
        title: "Авторизація",
        "email-label": "Електронна пошта:",
        "password-label": "Пароль:",
        "login-button": "Увійти",
        "login-button-google": "Увійти через Google",
        "login-button-facebook": "Увійти через Facebook",
        "registration": "Реєстрація",
        "registration-button": "Реєстрація",
        "forgot-password-button": "Забули пароль?",
        "message-ok": "Успішний вхід",
        "message-error": "Виникла помилка, будь ласка, спробуйте ще раз",
        "confirmation-message": "Код підтвердження надіслано на вашу пошту",
        "send-code-again": "Надіслати код знову",
        "invalid-code": "Невірний код, будь ласка, спробуйте ще раз",
        "password-mismatch": "Паролі не збігаються",
        "password-requirements": "Пароль має бути від 8 до 15 символів",
        "signup-title": "Реєстрація",
        "name-label": "Ім'я:",
        "surname-label": "Прізвище:",
        "confirm-password-label": "Підтвердьте пароль:",
        "signup-button": "Зареєструватися",
    }
};

function setLanguage(language) {
    document.querySelectorAll("[data-translate]").forEach(function(element) {
        const key = element.getAttribute("data-translate");
        element.innerText = translations[language][key];
    });

    // Установка выбранного языка в выпадающем списке
    const langSelect = document.getElementById('lang-select');
    if (langSelect) {
        langSelect.value = language;
    }

    // Сохранение выбранного языка в localStorage
    localStorage.setItem('selectedLanguage', language);
}

// Функция для переключения языков
function switchLanguage(language) {
    setLanguage(language);
}

// Detect browser language or set default to 'ru'
const userLang = navigator.language || navigator.userLanguage;
const defaultLang = localStorage.getItem('selectedLanguage') || 
                   (userLang.startsWith('ru') ? 'ru' : 
                   userLang.startsWith('en') ? 'en' : 
                   userLang.startsWith('zh') ? 'zh' : 'uk');

document.addEventListener('DOMContentLoaded', function() {
    // Set initial language
    setLanguage(defaultLang);
});


*/