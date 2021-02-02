var web3;

const accountBalance = async (address) => {
  var address, wei, balance

  let x = web3.eth.getBalance(address, function (error, wei) {
    if (!error) {
      var balance = window.web3.utils.fromWei(window.web3.utils.toBN(wei), 'ether');
      return balance; 
    } else {
      consloe.log(error)
    }
  })
  return x
}

// Restricts input for each element in the set of matched elements to the given inputFilter.
(function($) {
  $.fn.inputFilter = function(inputFilter) {
    return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function() {
      if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
      } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
      } else {
        this.value = "";
      }
    });
  };
}(jQuery));


$( document ).ready(function() {
  if (window.ethereum) {
    window.ethereum.on('chainChanged', chainId => {
      location.reload();
    })  
    web3.eth.net.getId()
      .then(function(network_id){
        if (network_id != 558){
          $('#btnNetworkTrigger').click();
        }
    })
  } else {
    $('#button-login').hide();
  }
  $('[data-toggle="tooltip"]').tooltip();
});
function gravatar_uri(address,size){
  return 'https://secure.gravatar.com/avatar/' + md5(address) +'.jpg?s='+size+'&d=identicon&r=g';
}
function profile_link(address,trim){
  if ($(window).width() <= 1440){
    trim=true;
  }
  if (trim){
    return '<a href="/profile/' + address + '" data-toggle="tooltip" title="Click here for more information."><span class="user-profile" style="padding-right:5px;"><img src="' + gravatar_uri(address,24) + '" alt="profile-image" class="gravatar" ></span>' + address.substring(0,6) + '...' + address.substring(36) + '</a>'
  } else {
    return '<a href="/profile/' + address + '" data-toggle="tooltip" title="Click here for more information."><span class="user-profile" style="padding-right:5px;"><img src="' + gravatar_uri(address,24) + '" alt="profile-image" class="gravatar" ></span>' + address + '</a>'
  }
}
String.prototype.capitalize = function() {
  x = this.toLowerCase();
  return x.charAt(0).toUpperCase() + x.slice(1)
}  
function secondsToHms(d) {
    d = Number(d);
    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);
    var s = Math.floor(d % 3600 % 60);

    var hDisplay = h > 0 ? h + (h == 1 ? "hr " : "hr ") : "";
    var mDisplay = m > 0 ? m + (m == 1 ? "min " : "min ") : "";
    var sDisplay = s > 0 ? s + (s == 1 ? "sec" : "sec") : "";
    return hDisplay + mDisplay + sDisplay; 
}

