   var ctx = document.getElementById('decorativeChart1').getContext('2d');     
       var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['01', '02', '03', '04', '05', '06'],
          datasets: [{
            data: [10, 18, 12, 8, 15, 10],
            backgroundColor: 'rgba(255, 255, 255, 0.12)',
            borderColor: '#fff',
            pointBackgroundColor:'#fff',
            pointHoverBackgroundColor:'#fff',
            pointBorderColor :'#fff',
            pointHoverBorderColor :'#fff',
            pointBorderWidth :1,
            pointRadius :0,
            pointHoverRadius :4,
            borderWidth: 2
          }]
        }
        ,
        options: {
      maintainAspectRatio: false,
              legend: {
                position: false,
                display: true,
            },
        tooltips: {
           enabled: false
      },
     scales: {
          xAxes: [{
            display: false,
            gridLines: false
          }],
          yAxes: [{
            display: false,
            gridLines: false
          }]
        }
        }
    
      });

   var ctx = document.getElementById('decorativeChart2').getContext('2d');
       var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['01', '02', '03', '04', '05', '06'],
          datasets: [{
            data: [10, 18, 12, 8, 15, 10],
            backgroundColor: 'rgba(255, 255, 255, 0.12)',
            borderColor: '#fff',
            pointBackgroundColor:'#fff',
            pointHoverBackgroundColor:'#fff',
            pointBorderColor :'#fff',
            pointHoverBorderColor :'#fff',
            pointBorderWidth :1,
            pointRadius :0,
            pointHoverRadius :4,
            borderWidth: 2
          }]
        }
        ,
        options: {
      maintainAspectRatio: false,
              legend: {
                position: false,
                display: true,
            },
        tooltips: {
           enabled: false
      },
     scales: {
          xAxes: [{
            display: false,
            gridLines: false
          }],
          yAxes: [{
            display: false,
            gridLines: false
          }]
        }
        }
    
      });
   var ctx = document.getElementById('decorativeChart3').getContext('2d');
       var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['01', '02', '03', '04', '05', '06'],
          datasets: [{
            data: [10, 18, 12, 8, 15, 10],
            backgroundColor: 'rgba(255, 255, 255, 0.12)',
            borderColor: '#fff',
            pointBackgroundColor:'#fff',
            pointHoverBackgroundColor:'#fff',
            pointBorderColor :'#fff',
            pointHoverBorderColor :'#fff',
            pointBorderWidth :1,
            pointRadius :0,
            pointHoverRadius :4,
            borderWidth: 2
          }]
        }
        ,
        options: {
      maintainAspectRatio: false,
              legend: {
                position: false,
                display: true,
            },
        tooltips: {
           enabled: false
      },
     scales: {
          xAxes: [{
            display: false,
            gridLines: false
          }],
          yAxes: [{
            display: false,
            gridLines: false
          }]
        }
        }
    
      });
  var chart9 = null;
  var options9 = {
      chart: {
        height: 250,
        type: 'radialBar',
        toolbar: {
          show: false
        }
      },
      plotOptions: {
        radialBar: {
          //startAngle: -135,
          //endAngle: 225,
           hollow: {
            margin: 0,
            size: '85%',
            background: 'transparent',
            image: undefined,
            imageOffsetX: 0,
            imageOffsetY: 0,
            position: 'front',
            dropShadow: {
              enabled: true,
              top: 3,
              left: 0,
              blur: 4,
              //color: 'rgba(8, 165, 14, 0.65)',
              opacity: 0.12
            }
          },
          track: {
            background: 'rgba(255, 255, 255, 0.12)',
            strokeWidth: '30%',
            margin: 0, // margin is in pixels
            dropShadow: {
              enabled: true,
              top: -3,
              left: 0,
              blur: 4,
        //color: 'rgba(8, 165, 14, 0.65)',
              opacity: 0.12
            }
          },

          dataLabels: { 
            showOn: 'always',
            name: {
              offsetY: -20,
              show: true,
              color: '#fff',
              fontSize: '15px'
            },
            value: {
              formatter: function (val) {
            return val + "%";
          },
              color: '#fff',
              fontSize: '40px',
              show: true,
        offsetY: 10,
            }
          }
        }
      },
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'light',
          type: 'horizontal',
          shadeIntensity: 0.5,
          gradientToColors: ['#08a50e'],
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100]
        }
      },
      colors: ["#cddc35"],
      series: [ ],
      stroke: {
        //lineCap: 'round',
        dashArray: 4
      },
      labels: ['Circulation Locked'],

    }

  var chart10 = null;
  var options10 = {
    chart: {
      height: 250,
      type: 'radialBar',
      toolbar: {
        show: false
      },
      animations: {
        enabled: false,
      },
    },
    plotOptions: {
      radialBar: {
        //startAngle: -135,
        //endAngle: 225,
         hollow: {
          margin: 0,
          size: '85%',
          background: 'transparent',
          image: undefined,
          imageOffsetX: 0,
          imageOffsetY: 0,
          position: 'front',
          dropShadow: {
            enabled: true,
            top: 3,
            left: 0,
            blur: 4,
            //color: 'rgba(246, 181, 49, 0.65)',
            opacity: 0.12
          }
        },
        track: {
          background: 'rgba(255, 255, 255, 0.12)',
          strokeWidth: '30%',
          margin: 0, // margin is in pixels
          dropShadow: {
            enabled: true,
            top: -3,
            left: 0,
            blur: 4,
      //color: 'rgba(246, 181, 49, 0.65)',
            opacity: 0.12
          }
        },

        dataLabels: { 
          showOn: 'always',
          name: {
            offsetY: -20,
            show: true,
            color: '#fff',
            fontSize: '15px'
          },
          value: {
            formatter: function (val) {
          return val + "%";
        },
            color: '#fff',
            fontSize: '40px',
            show: true,
      offsetY: 10,
          }
        }
      }
    },
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'light',
          type: 'horizontal',
          shadeIntensity: 0.5,
          gradientToColors: ['#cddc35'],
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100]
        }
      },
      colors: ["#08a50e"],
    series: [  ],
    stroke: {
      //lineCap: 'round',
      dashArray: 4
    },
    labels: ['Quorum Filled'],
  }
  var chart11 = null;
  var options11 = {
    chart: {
      height: 250,
      type: 'radialBar',
      toolbar: {
        show: false
      }
    },
    plotOptions: {
      radialBar: {
        //startAngle: -135,
        //endAngle: 225,
         hollow: {
          margin: 0,
          size: '85%',
          background: 'transparent',
          image: undefined,
          imageOffsetX: 0,
          imageOffsetY: 0,
          position: 'front',
          dropShadow: {
            enabled: true,
            top: 3,
            left: 0,
            blur: 4,
            //color: 'rgba(246, 181, 49, 0.65)',
            opacity: 0.12
          }
        },
        track: {
          background: 'rgba(255, 255, 255, 0.12)',
          strokeWidth: '30%',
          margin: 0, // margin is in pixels
          dropShadow: {
            enabled: true,
            top: -3,
            left: 0,
            blur: 4,
      //color: 'rgba(246, 181, 49, 0.65)',
            opacity: 0.12
          }
        },

        dataLabels: { 
          showOn: 'always',
          name: {
            offsetY: -20,
            show: true,
            color: '#fff',
            fontSize: '15px'
          },
          value: {
            formatter: function (val) {
          return val + "%";
        },
            color: '#fff',
            fontSize: '40px',
            show: true,
      offsetY: 10,
          }
        }
      }
    },
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'light',
          type: 'horizontal',
          shadeIntensity: 0.5,
          gradientToColors: ['#8f50ff'],
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100]
        }
      },
      colors: ["#d13adf"],
    series: [  ],
    stroke: {
      //lineCap: 'round',
      dashArray: 4
    },
    labels: ['Avg Validator ROI'],
  }
  var chart12 = null;
  var options12 = {
    chart: {
      height: 250,
      type: 'radialBar',
      toolbar: {
        show: false
      }
    },
    plotOptions: {
      radialBar: {
        //startAngle: -135,
        //endAngle: 225,
         hollow: {
          margin: 0,
          size: '85%',
          background: 'transparent',
          image: undefined,
          imageOffsetX: 0,
          imageOffsetY: 0,
          position: 'front',
          dropShadow: {
            enabled: true,
            top: 3,
            left: 0,
            blur: 4,
            //color: 'rgba(246, 181, 49, 0.65)',
            opacity: 0.12
          }
        },
        track: {
          background: 'rgba(255, 255, 255, 0.12)',
          strokeWidth: '30%',
          margin: 0, // margin is in pixels
          dropShadow: {
            enabled: true,
            top: -3,
            left: 0,
            blur: 4,
      //color: 'rgba(246, 181, 49, 0.65)',
            opacity: 0.12
          }
        },

        dataLabels: { 
          showOn: 'always',
          name: {
            offsetY: -20,
            show: true,
            color: '#fff',
            fontSize: '15px'
          },
          value: {
            formatter: function (val) {
          return val + "%";
        },
            color: '#fff',
            fontSize: '40px',
            show: true,
      offsetY: 10,
          }
        }
      }
    },
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'light',
        type: 'horizontal',
        shadeIntensity: 0.5,
        gradientToColors: ['#f7b733'],
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 100]
      }
    },
    colors: ["#fc4a1a"],
    series: [  ],
    stroke: {
      //lineCap: 'round',
      dashArray: 4
    },
    labels: ['Avg Voter ROI'],
  }

