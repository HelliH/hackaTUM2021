$("#select-region").on("change", function () {
  let optionsMicro;
  let regionId = $(this).find("option:selected").attr("id");
  if (regionId != "region0") {
    optionsMicro = getMicros(regionId);
  }
  $("#select-micro option").remove();
  $("#select-micro").append(optionsMicro);
});

function getMicros(regionId) {
  let micro = [];
  let optionsMicro =
    '<option id="micro0" value="value0" disabled selected>Select a microscope</option>';

  switch (regionId) {
    case "region1":
      micro = ["MICDEV013"];
      break;
    case "region2":
      micro = [
        "MICDEV05",
        "MICDEV016",
        "MICDEV00",
        "MICDEV06",
        "MICDEV018",
        "MICDEV012",
        "MICDEV02",
        "MICDEV011",
        "MICDEV017",
      ];
      break;
    case "region3":
      micro = [
        "MICDEV03",
        "MICDEV01",
        "MICDEV014",
        "MICDEV09",
        "MICDEV021",
        "MICDEV08",
      ];
      break;
    case "region4":
      micro = [
        "MICDEV010",
        "MICDEV015",
        "MICDEV022",
        "MICDEV07",
        "MICDEV04",
        "MICDEV023",
        "MICDEV020",
        "MICDEV019",
      ];
      break;
  }

  micro.forEach((element, index) => {
    optionsMicro += `<option id="micro${
      index + 1
    }" value="value${index}">${element}</option>`;
  });

  return optionsMicro;
}

$("#select-micro").on("change", function () {
  let regionName = $("#select-region").find("option:selected").text();
  let microName = $(this).find("option:selected").text();

  if (microName != "Select a microscope") {
    $(".iframe-block").remove();
    $(".skills-page").append(
      `
        <div class="iframe-block">
          <div class="region-micro">
            <div class="region-micro-slider">
             <div>
              <img src="img/graphics/AllPeriod_${regionName}_${microName}__sensors_coverage.png" alt="">
              <span>sensor coverage over all period</span>
             </div>
            <div>
              <img src="img/graphics/20days_${regionName}_${microName}__sensors_coverage.png" alt="">
              <span>sensor coverage over last 20 days</span>
            </div>
            </div>
          </div>
        </div>`
    );
    sliderGraphics();
  }
});

// Плавная прокрутка
function jackor() {
  $(document).ready(function () {
    $(".header__nav .header__item").on("click", "a", function (event) {
      event.preventDefault();
      var id = $(this).attr("href"),
        top = $(id).offset().top;
      $("body,html").animate({ scrollTop: top }, 700);
    });
    $(".button-1").on("click", $(this), function (event) {
      event.preventDefault();
      var id = $(this).attr("href"),
        top = $(id).offset().top;
      $("body,html").animate({ scrollTop: top }, 700);
    });
  });
}

// Слайдер графиков
function sliderGraphics() {
  $(".region-micro-slider").slick({
    slidesToShow: 1,
    centerMode: true,
    arrows: false,
    autoplay: true,
    autoplaySpeed: 3000,
  });
}

// Слайдер на главной
function slider() {
  $(".main-page__desc-img").slick({
    slidesToShow: 1,
    centerMode: true,
    arrows: false,
    autoplay: true,
    autoplaySpeed: 3000,
  });
}

// Добавление классов для Бургера
function activenav() {
  $(".header__burger").click(function (event) {
    $(".header__burger, .header__nav").toggleClass("active");
  });
}

// Скролл наверх
function scrollToTop() {
  if ($("#back-to-top").length) {
    var scrollTrigger = 100,
      backToTop = function () {
        var scrollTop = $(window).scrollTop();
        if (scrollTop > scrollTrigger) {
          $("#back-to-top").addClass("show");
        } else {
          $("#back-to-top").removeClass("show");
        }
      };
    backToTop();
    $(window).on("scroll", function () {
      backToTop();
    });
    $("#back-to-top").on("click", function (e) {
      e.preventDefault();
      $("html,body").animate(
        {
          scrollTop: 0,
        },
        400
      );
    });
  }
}

$(document).ready(function () {
  jackor();
  slider();
  activenav();
  scrollToTop();
});
