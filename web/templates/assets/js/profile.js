  function getBalance(address) {
    if (!address) return 0
    
    var address, wei

    const balance = accountBalance(address);
    balance.then(function(b){
      const bal = nf.format(parseFloat(window.web3.utils.fromWei(b,'ether')).toFixed(8));
    })
  }
   var options1 = {
      chart: {
        height: 200,
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
            size: '70%',
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
              opacity: 0.24
            }
          },
          track: {
            background: 'rgba(255, 255, 255, 0.12)',
            strokeWidth: '67%',
            margin: 0, // margin is in pixels
            dropShadow: {
              enabled: true,
              top: -3,
              left: 0,
              blur: 4,
              opacity: 0.35
            }
          },

          dataLabels: {
            showOn: 'always',
            name: {
              offsetY: -0,
              show: false,
              color: '#fff',
              fontSize: '16px'
            },
            value: {
              formatter: function(val) {
                return val + "%";
              },
        offsetY: 8,
              color: '#fff',
              fontSize: '19px',
              show: true,
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
          gradientToColors: ['#f1076f'],
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100]
        }
      },
      colors: ["#ff5447"],
      series: [ ],
      stroke: {
        lineCap: 'round'
      },
      labels: ['Percent'],
      responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        height: 230
                    }
                }
            }]
    }
   var options2 = {
      chart: {
        height: 200,
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
            size: '70%',
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
              opacity: 0.24
            }
          },
          track: {
            background: 'rgba(255, 255, 255, 0.12)',
            strokeWidth: '67%',
            margin: 0, // margin is in pixels
            dropShadow: {
              enabled: true,
              top: -3,
              left: 0,
              blur: 4,
              opacity: 0.35
            }
          },

          dataLabels: {
            showOn: 'always',
            name: {
              offsetY: -0,
              show: false,
              color: '#fff',
              fontSize: '16px'
            },
            value: {
              formatter: function(val) {
                return val + "%";
              },
        offsetY: 8,
              color: '#fff',
              fontSize: '19px',
              show: true,
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
          gradientToColors: ['#0072ff'],
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100]
        }
      },
      colors: ["#00c8ff"],
      series: [45],
      stroke: {
        lineCap: 'round'
      },
      labels: ['Percent'],
      responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        height: 230
                    }
                }
            }]
    }
   var options3 = {
      chart: {
        height: 200,
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
            size: '70%',
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
              opacity: 0.24
            }
          },
          track: {
            background: 'rgba(255, 255, 255, 0.12)',
            strokeWidth: '67%',
            margin: 0, // margin is in pixels
            dropShadow: {
              enabled: true,
              top: -3,
              left: 0,
              blur: 4,
              opacity: 0.35
            }
          },

          dataLabels: {
            showOn: 'always',
            name: {
              offsetY: -0,
              show: false,
              color: '#fff',
              fontSize: '16px'
            },
            value: {
              formatter: function(val) {
                return val + "%";
              },
        offsetY: 8,
              color: '#fff',
              fontSize: '19px',
              show: true,
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
          gradientToColors: ['#f7971e'],
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100]
        }
      },
      colors: ["#ffd200"],
      series: [55],
      stroke: {
        lineCap: 'round'
      },
      labels: ['Percent'],
      responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        height: 230
                    }
                }
            }]
    }
   var options4 = {
      chart: {
        height: 200,
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
            size: '70%',
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
              opacity: 0.24
            }
          },
          track: {
            background: 'rgba(255, 255, 255, 0.12)',
            strokeWidth: '67%',
            margin: 0, // margin is in pixels
            dropShadow: {
              enabled: true,
              top: -3,
              left: 0,
              blur: 4,
              opacity: 0.35
            }
          },

          dataLabels: {
            showOn: 'always',
            name: {
              offsetY: -0,
              show: false,
              color: '#fff',
              fontSize: '16px'
            },
            value: {
              formatter: function(val) {
                return val + "%";
              },
        offsetY: 8,
              color: '#fff',
              fontSize: '19px',
              show: true,
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
      series: [80],
      stroke: {
        lineCap: 'round'
      },
      labels: ['Percent'],
      responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        height: 230
                    }
                }
            }]
    }

$(function() {
    "use strict";
    window.Apex = {
      stroke: {
        width: 3
      },
      markers: {
        size: 0
      },
      tooltip: {
        fixed: {
          enabled: true,
        }
      }
    };
    
    var randomizeArray = function (arg) {
      var array = arg.slice();
      var currentIndex = array.length,
        temporaryValue, randomIndex;

      while (0 !== currentIndex) {

        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
      }

      return array;
    }
});


