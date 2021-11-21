Vue.component('portfolio-list__item', {
  props: ['portfolio'],
  template: `
  <div class="portfolio-list__item"
  @mouseover="updatePortfolio"
  >
  <div class="portfolio-list__img">
  <img :src="portfolio.portfolioImage" alt="">
  </div>
  <div class="portfolio-list__text">
  {{ portfolio.portfolioName }}
  </div>
  </div>
  `,
  data() {
    return {

    }
  },
  methods: {
    updatePortfolio: function() {
      this.$emit('update-portfolio', this.portfolio.portfolioImage, this.portfolio.portfolioText)
    },
  },
  computed: {

  }
})

var app = new Vue({
  el: '#app',
  data: {
    image: "./img/No_anomalies.png",
    id: 0,
    portfolios: [
      {
        portfolioName: "Inbound prediction",
        portfolioId: 1,
        portfolioImage: "./img/No_anomalies.png",
      },
      {
        portfolioName: "Anomaly Detection",
        portfolioId: 2,
        portfolioImage: "./img/Anomaly.png",
      },
      // {
      //   portfolioName: "График 3",
      //   portfolioId: 3,
      //   portfolioImage: "./img/555.png",
      //   portfolioLink: "http://m95215kf.beget.tech/internet-resheniya/index.html"
      // },
      // {
      //   portfolioName: "График 4",
      //   portfolioId: 4,
      //   portfolioImage: "./img/333.png",
      //   portfolioLink: "http://m95215kf.beget.tech/test2/index.html"
      // },
      // {
      //   portfolioName: "График 5",
      //   portfolioId: 5,
      //   portfolioImage: "./img/444.png",
      //   portfolioLink: "http://m95215kf.beget.tech/test33/index.html"
      // },
    ],
  },
  methods: {
    updateportfolio(portfolioImage, portfolioText) {
      this.image = portfolioImage,
      this.text = portfolioText
    },
  }
})
