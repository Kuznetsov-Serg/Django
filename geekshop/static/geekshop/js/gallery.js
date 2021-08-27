
/*
*******************************************************************************************
    ГАЛЕРЕЯ
*******************************************************************************************
*/

/**
 * @property {Object} settings Объект с настройками галереи.
                        * @property {string} settings.previewSelector Селектор обертки для миниатюр галереи.
                        * @property {string} settings.openedImageWrapperClass Класс для обертки открытой картинки.
                        * @property {string} settings.openedImageClass Класс открытой картинки.
                        * @property {string} settings.openedImageScreenClass Класс для ширмы открытой картинки.
                        * @property {string} settings.openedImageCloseBtnClass Класс для картинки кнопки закрыть.
                        * @property {string} settings.openedImageCloseBtnSrc Путь до картинки кнопки открыть.
                        * @property {string} settings.openedImageNextBtnSrc Путь до картинки со стрелкой вправо.
                        * @property {string} settings.openedImageNextBtnClass Класс картинки со стрелкой вправо.
                        * @property {string} settings.openedImageBackBtnSrc Путь до картинки со стрелкой влево.
                        * @property {string} settings.openedImageBackBtnClass Класс картинки со стрелкой влево.
                        * @property {string} settings.imageNotFoundSrc Путь до стандартной картинки-заглушки.
                        * @property {string} settings.openedImageBackBtnSrc Путь до каталога вспомогательных картинок .
                        */
const gallery = {
    openedImageEl: null,
    arrImg: [],

    settings: {
        previewSelector: '.mySuperGallery',
        openedImageWrapperClass: 'galleryWrapper',
        openedImageClass: 'galleryWrapper__image',
        openedImageScreenClass: 'galleryWrapper__screen',
        openedImageCloseBtnClass: 'galleryWrapper__close',
        openedImageCloseBtnSrc: 'крестик.png',
        openedImageNextBtnSrc: 'arrow_right_red.png',
        openedImageNextBtnClass: 'galleryWrapper__next',
        openedImageBackBtnSrc: 'arrow_left_red.png',
        openedImageBackBtnClass: 'galleryWrapper__back',
        imageNotFoundSrc: 'duck.gif',
        imageBasePathSrc: 'img/',
    },

    /**
     * Инициализирует галерею, ставит обработчик события.
     * @param {Object} settings Объект настроек для галереи.
                        */
    init(settings) {
        // Записываем настройки, которые передал пользователь в наши настройки.
        this.settings = Object.assign(this.settings, settings);

        this.addPathScr()   // Добавим к названию картинок кнопок путь

        // Находим элемент, где будут превью картинок и ставим обработчик на этот элемент,
        // при клике на этот элемент вызовем функцию containerClickHandler в нашем объекте
        // gallery и передадим туда событие MouseEvent, которое случилось.
        if (document.querySelector(this.settings.previewSelector))
            document
                .querySelector(this.settings.previewSelector)
                .addEventListener('click', event => this.containerClickHandler(event));
    },

    // Добавим к названию картинок кнопок путь
    addPathScr() {
        if (this.settings.imageBasePathSrc != '') {
            this.settings.openedImageCloseBtnSrc = this.settings.imageBasePathSrc + this.settings.openedImageCloseBtnSrc;   //Путь до картинки кнопки открыть.
            this.settings.openedImageNextBtnSrc = this.settings.imageBasePathSrc + this.settings.openedImageNextBtnSrc;     //Путь до картинки со стрелкой вправо.
            this.settings.openedImageBackBtnSrc = this.settings.imageBasePathSrc + this.settings.openedImageBackBtnSrc;     // Путь до картинки со стрелкой влево.
            this.settings.imageNotFoundSrc = this.settings.imageBasePathSrc + this.settings.imageNotFoundSrc;               // Путь до стандартной картинки-заглушки.
            this.settings.imageBasePathSrc = '';
        }
    },

    /**
     * Обработчик события клика для открытия картинки.
     * @param {MouseEvent} event Событие клики мышью.
                        * @param {HTMLElement} event.target Событие клики мышью.
                        */
    containerClickHandler(event) {
        // Если целевой тег не был картинкой, то ничего не делаем, просто завершаем функцию.
        if (event.target.tagName !== 'IMG') {
            return;
        }

        // Записываем текущую картинку, которую хотим открыть.
        this.openedImageEl = event.target;

        // Открываем картинку.
        this.openImage(event.target.dataset.full_image_url);
    },

    /**
     * Открывает картинку.
     * @param {string} src Ссылка на картинку, которую надо открыть.
                        * Переделал на массив ссылок
                        */
    openImage(src) {
//        console.log('src=', src)
        // Пробуем загрузить картинку, если картинка загружена - показываем картинку с полученным из
        // целевого тега (data-full_image_url аттрибут), если картинка не загрузилась - показываем картинку-заглушку.
        // Получаем контейнер для открытой картинки, в нем находим тег img и ставим ему нужный src.
        const openedImageEl = this.getScreenContainer().querySelector(`.${this.settings.openedImageClass}`);
        const img = new Image();

        if (Array.isArray(src)) this.arrImg = JSON.parse(JSON.stringify(src));  // глубокое клонирование
        else this.arrImg = src.split(',');

        // this.arrImg = JSON.parse(JSON.stringify(src)).split(',');     // глубокое клонирование
        const src0 = this.arrImg[0];
        if (src0)
            img.onload = () => openedImageEl.src = src0;
        img.onerror = () => openedImageEl.src = this.settings.imageNotFoundSrc;
        img.src = src0;

        const backBtn = document.querySelector(`.${this.settings.openedImageBackBtnClass}`);
        const nextBtn = document.querySelector(`.${this.settings.openedImageNextBtnClass}`);
        if (this.isArrayImg()) {      // Картинок несколько - включим кнопки "предыдущая" и "следующая"
            backBtn.style = "display:''";
            nextBtn.style = "display:''";
        } else {
            backBtn.style = "display:none";
            nextBtn.style = "display:none";
        }
    },

    // Определяем, несколько картинок? (влияет на показ кнопок "следующая" и "предыдущая")
    isArrayImg() {
        return this.arrImg.length > 1
    },

    /**
     * Возвращает контейнер для открытой картинки, либо создает такой контейнер, если его еще нет.
     * @returns {Element}
                        */
    getScreenContainer() {
        // Получаем контейнер для открытой картинки.
        const galleryWrapperElement = document.querySelector(`.${this.settings.openedImageWrapperClass}`);
        // Если контейнер для открытой картинки существует - возвращаем его.
        if (galleryWrapperElement) {
            return galleryWrapperElement;
        }

        // Возвращаем полученный из метода createScreenContainer контейнер.
        return this.createScreenContainer();
    },

    /**
     * Создает контейнер для открытой картинки.
     * @returns {HTMLElement}
                        */
    createScreenContainer() {
        // Создаем сам контейнер-обертку и ставим ему класс.
        let galleryWrapperElement = document.createElement('div');
        galleryWrapperElement.classList.add(this.settings.openedImageWrapperClass);
        // let target = document.querySelector('.education_body');
        // target.insertAdjacentElement('beforeBegin', galleryWrapperElement);
        // galleryWrapperElement.insertAdjacentElement('beforeBegin', document.body);
        // Добавляем кнопку назад.
        const backBtn = new Image();
        backBtn.classList.add(this.settings.openedImageBackBtnClass);
        backBtn.src = this.settings.openedImageBackBtnSrc;
        galleryWrapperElement.appendChild(backBtn);

        // Добавляем обработчик события при клике, ставим новую открытую картинку и открываем ее.
        backBtn.addEventListener('click', () => {
            this.getPrevImage_();                   // переделал на массив
            this.openImage(this.arrImg);
            // this.openedImageEl = this.getPrevImage();
            // this.openImage(this.openedImageEl.dataset.full_image_url);
        });

        // Добавляем кнопку вперед.
        const nextBtn = new Image();
        nextBtn.classList.add(this.settings.openedImageNextBtnClass);
        nextBtn.src = this.settings.openedImageNextBtnSrc;
        galleryWrapperElement.appendChild(nextBtn);

        // Добавляем обработчик события при клике, ставим новую открытую картинку и открываем ее.
        nextBtn.addEventListener('click', () => {
            this.getNextImage_();                   // переделал на массив
            this.openImage(this.arrImg);
            // this.openedImageEl = this.getNextImage();
            // this.openImage(this.openedImageEl.dataset.full_image_url);
        });

        // Создаем контейнер занавеса, ставим ему класс и добавляем в контейнер-обертку.
        const galleryScreenElement = document.createElement('div');
        galleryScreenElement.classList.add(this.settings.openedImageScreenClass);
        galleryWrapperElement.appendChild(galleryScreenElement);

        // Создаем картинку для кнопки закрыть, ставим класс, src и добавляем ее в контейнер-обертку.
        const closeImageElement = new Image();
        closeImageElement.classList.add(this.settings.openedImageCloseBtnClass);
        closeImageElement.src = this.settings.openedImageCloseBtnSrc;
        closeImageElement.addEventListener('click', () => this.close());
        galleryWrapperElement.appendChild(closeImageElement);

        // Создаем картинку, которую хотим открыть, ставим класс и добавляем ее в контейнер-обертку.
        const image = new Image();
        image.classList.add(this.settings.openedImageClass);
        galleryWrapperElement.appendChild(image);

        // Добавляем контейнер-обертку в тег body.
        document.body.appendChild(galleryWrapperElement);

        // Возвращаем добавленный в body элемент, наш контейнер-обертку.
        return galleryWrapperElement;
    },

    /**
     * Возвращает следующий элемент (картинку) от открытой или первую картинку в контейнере,
     * если текущая открытая картинка последняя.
     * @returns {Element} Следующую картинку от текущей открытой.
                        */
    getNextImage_() {
        // Переделал метод на взятие картинки из массива (прокрутим массив)
        this.arrImg.push(this.arrImg[0]);   // перенесем первую картинку в конец
        this.arrImg.shift();                // и удалим её с начала массива
    },
    getNextImage() {
        // Переделал метод на взятие картинки из массива 
        this.arrImg.push(this.arrImg[0]);
        return
        // Получаем элемент справа от текущей открытой картинки.
        const nextSibling = this.openedImageEl.nextElementSibling;
        // Если элемент справа есть, его отдаем, если нет, то берем первый элемент в родительском контейнере.
        return nextSibling ? nextSibling : this.openedImageEl.parentElement.firstElementChild;
    },

    /**
     * Возвращает предыдущий элемент (картинку) от открытой или последнюю картинку в контейнере,
     * если текущая открытая картинка первая.
     * @returns {Element} Предыдущую картинку от текущей открытой.
                        */
    getPrevImage_() {
        // Переделал метод на взятие картинки из массива 
        this.arrImg.unshift(this.arrImg.pop());   // перенесем последнюю картинку в начало
    },
    getPrevImage() {
        // Получаем элемент слева от текущей открытой картинки.
        const prevSibling = this.openedImageEl.previousElementSibling;
        // Если элемент слева есть, его отдаем, если нет, то берем последний элемент в родительском контейнере.
        if (prevSibling) {
            return prevSibling;
        } else {
            return this.openedImageEl.parentElement.lastElementChild;
        }
    },

    /**
     * Закрывает (удаляет) контейнер для открытой картинки.
     */
    close() {
        document.querySelector(`.${this.settings.openedImageWrapperClass}`).remove();
    }
};