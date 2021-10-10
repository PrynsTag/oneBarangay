const d = document;
d.addEventListener('DOMContentLoaded', (event) => {
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-primary me-3',
      cancelButton: 'btn btn-gray',
    },
    buttonsStyling: false,
  });

  const themeSettingsEl = document.getElementById('theme-settings');
  const themeSettingsExpandEl = document.getElementById('theme-settings-expand');

  if (themeSettingsEl) {
    const themeSettingsCollapse = new bootstrap.Collapse(themeSettingsEl, {
      show: true,
      toggle: false,
    });

    if (window.localStorage.getItem('settings_expanded') === 'true') {
      themeSettingsCollapse.show();
      themeSettingsExpandEl.classList.remove('show');
    } else {
      themeSettingsCollapse.hide();
      themeSettingsExpandEl.classList.add('show');
    }

    themeSettingsEl.addEventListener('hidden.bs.collapse', () => {
      themeSettingsExpandEl.classList.add('show');
      window.localStorage.setItem('settings_expanded', false);
    });

    themeSettingsExpandEl.addEventListener('click', () => {
      themeSettingsExpandEl.classList.remove('show');
      window.localStorage.setItem('settings_expanded', true);
      setTimeout(() => {
        themeSettingsCollapse.show();
      }, 300);
    });
  }

  // options
  const breakpoints = {
    sm: 540,
    md: 720,
    lg: 960,
    xl: 1140,
  };

  const sidebar = document.getElementById('sidebarMenu');
  if (sidebar && d.body.clientWidth < breakpoints.lg) {
    sidebar.addEventListener('shown.bs.collapse', () => {
      document.querySelector('body').style.position = 'fixed';
    });
    sidebar.addEventListener('hidden.bs.collapse', () => {
      document.querySelector('body').style.position = 'relative';
    });
  }

  const iconNotifications = d.querySelector('.notification-bell');
  if (iconNotifications) {
    iconNotifications.addEventListener('shown.bs.dropdown', () => {
      iconNotifications.classList.remove('unread');
    });
  }

  [].slice.call(d.querySelectorAll('[data-background]')).map((el) => {
    el.style.background = `url(${el.getAttribute('data-background')})`;
  });

  [].slice.call(d.querySelectorAll('[data-background-lg]')).map((el) => {
    if (document.body.clientWidth > breakpoints.lg) {
      el.style.background = `url(${el.getAttribute('data-background-lg')})`;
    }
  });

  [].slice.call(d.querySelectorAll('[data-background-color]')).map((el) => {
    el.style.background = `url(${el.getAttribute('data-background-color')})`;
  });

  [].slice.call(d.querySelectorAll('[data-color]')).map((el) => {
    el.style.color = `url(${el.getAttribute('data-color')})`;
  });

  // Tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  const tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl));

  // Popovers
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  const popoverList = popoverTriggerList.map((popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl));

  // Datepicker
  const datepickers = [].slice.call(d.querySelectorAll('[data-datepicker]'));
  const datepickersList = datepickers.map((el) => new Datepicker(el, {
    buttonClass: 'btn',
  }));

  if (d.querySelector('.input-slider-container')) {
    [].slice.call(d.querySelectorAll('.input-slider-container')).map((el) => {
      const slider = el.querySelector(':scope .input-slider');
      const sliderId = slider.getAttribute('id');
      const minValue = slider.getAttribute('data-range-value-min');
      const maxValue = slider.getAttribute('data-range-value-max');

      const sliderValue = el.querySelector(':scope .range-slider-value');
      const sliderValueId = sliderValue.getAttribute('id');
      const startValue = sliderValue.getAttribute('data-range-value-low');

      const c = d.getElementById(sliderId);
      const id = d.getElementById(sliderValueId);

      noUiSlider.create(c, {
        start: [parseInt(startValue)],
        connect: [true, false],
        // step: 1000,
        range: {
          min: [parseInt(minValue)],
          max: [parseInt(maxValue)],
        },
      });
    });
  }

  if (d.getElementById('input-slider-range')) {
    const c = d.getElementById('input-slider-range');
    const low = d.getElementById('input-slider-range-value-low');
    const e = d.getElementById('input-slider-range-value-high');
    const f = [d, e];

    noUiSlider.create(c, {
      start: [parseInt(low.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
      connect: !0,
      tooltips: true,
      range: {
        min: parseInt(c.getAttribute('data-range-value-min')),
        max: parseInt(c.getAttribute('data-range-value-max')),
      },
    }), c.noUiSlider.on('update', (a, b) => {
      f[b].textContent = a[b];
    });
  }

  // Chartist

  if (d.querySelector('.ct-chart-sales-value')) {
    // Chart 5
    new Chartist.Line('.ct-chart-sales-value', {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      series: [
        [0, 10, 30, 40, 80, 60, 100],
      ],
    }, {
      low: 0,
      showArea: true,
      fullWidth: true,
      plugins: [
        Chartist.plugins.tooltip(),
      ],
      axisX: {
        // On the x-axis start means top and end means bottom
        position: 'end',
        showGrid: true,
      },
      axisY: {
        // On the y-axis start means left and end means right
        showGrid: false,
        showLabel: false,
        labelInterpolationFnc(value) {
          return `$${value / 1}k`;
        },
      },
    });
  }

  if (d.querySelector('.ct-chart-ranking')) {
    const chart = new Chartist.Bar('.ct-chart-ranking', {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      series: [
        [1, 5, 2, 5, 4, 3],
        [2, 3, 4, 8, 1, 2],
      ],
    }, {
      low: 0,
      showArea: true,
      plugins: [
        Chartist.plugins.tooltip(),
      ],
      axisX: {
        // On the x-axis start means top and end means bottom
        position: 'end',
      },
      axisY: {
        // On the y-axis start means left and end means right
        showGrid: false,
        showLabel: false,
        offset: 0,
      },
    });

    chart.on('draw', (data) => {
      if (data.type === 'line' || data.type === 'area') {
        data.element.animate({
          d: {
            begin: 2000 * data.index,
            dur: 2000,
            from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
            to: data.path.clone().stringify(),
            easing: Chartist.Svg.Easing.easeOutQuint,
          },
        });
      }
    });
  }

  if (d.querySelector('.ct-chart-traffic-share')) {
    const data = {
      series: [70, 20, 10],
    };

    const sum = function (a, b) {
      return a + b;
    };

    new Chartist.Pie('.ct-chart-traffic-share', data, {
      labelInterpolationFnc(value) {
        return `${Math.round(value / data.series.reduce(sum) * 100)}%`;
      },
      low: 0,
      high: 8,
      donut: true,
      donutWidth: 20,
      donutSolid: true,
      fullWidth: false,
      showLabel: false,
      plugins: [
        Chartist.plugins.tooltip(),
      ],
    });
  }

  if (d.getElementById('loadOnClick')) {
    d.getElementById('loadOnClick').addEventListener('click', function () {
      const button = this;
      const loadContent = d.getElementById('extraContent');
      const allLoaded = d.getElementById('allLoadedText');

      button.classList.add('btn-loading');
      button.setAttribute('disabled', 'true');

      setTimeout(() => {
        loadContent.style.display = 'block';
        button.style.display = 'none';
        allLoaded.style.display = 'block';
      }, 1500);
    });
  }

  const scroll = new SmoothScroll('a[href*="#"]', {
    speed: 500,
    speedAsDuration: true,
  });

  if (d.querySelector('.current-year')) {
    d.querySelector('.current-year').textContent = new Date().getFullYear();
  }

  // Glide JS

  if (d.querySelector('.glide')) {
    new Glide('.glide', {
      type: 'carousel',
      startAt: 0,
      perView: 3,
    }).mount();
  }

  if (d.querySelector('.glide-testimonials')) {
    new Glide('.glide-testimonials', {
      type: 'carousel',
      startAt: 0,
      perView: 1,
      autoplay: 2000,
    }).mount();
  }

  if (d.querySelector('.glide-clients')) {
    new Glide('.glide-clients', {
      type: 'carousel',
      startAt: 0,
      perView: 5,
      autoplay: 2000,
    }).mount();
  }

  if (d.querySelector('.glide-news-widget')) {
    new Glide('.glide-news-widget', {
      type: 'carousel',
      startAt: 0,
      perView: 1,
      autoplay: 2000,
    }).mount();
  }

  if (d.querySelector('.glide-autoplay')) {
    new Glide('.glide-autoplay', {
      type: 'carousel',
      startAt: 0,
      perView: 3,
      autoplay: 2000,
    }).mount();
  }

  // Pricing countup
  const billingSwitchEl = d.getElementById('billingSwitch');
  if (billingSwitchEl) {
    const countUpStandard = new countUp.CountUp('priceStandard', 99, { startVal: 199 });
    const countUpPremium = new countUp.CountUp('pricePremium', 199, { startVal: 299 });

    billingSwitchEl.addEventListener('change', () => {
      if (billingSwitch.checked) {
        countUpStandard.start();
        countUpPremium.start();
      } else {
        countUpStandard.reset();
        countUpPremium.reset();
      }
    });
  }
});
