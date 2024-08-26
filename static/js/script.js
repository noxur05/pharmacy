document.addEventListener('DOMContentLoaded', function () {
    // Initialize Carousel 1
    new Splide('#carousel-ads', {
        arrows: false,
        pagination: false,
        gap: "1.5rem",
        type: 'loop',
        autoplay: true,
        rewind: true,
        type: 'fade',
    }).mount();

    $(document).ready(function() {
        $('[data-fancybox]').fancybox({
            // Custom options
        });
    });

    document.querySelectorAll('.splide-goods').forEach(function (element) {
        new Splide(element, {
            arrows: true,
            pagination: false,
            perPage: 5,
            gap: "1.5rem",
            breakpoints: {
                1200: {
                    perPage: 5
                },
                992: {
                    perPage: 4,
                    gap: "1.2rem"
                },
                768: {
                    perPage: 3,
                    gap: "1rem"
                },
                576: {
                    perPage: 2,
                    gap: "1rem"
                },
                330: {
                    perPage: 1,
                    gap: "1rem"
                },
              },
            focus: 0,
            omitEnd: true
        }).mount();

        const id = element.id;
        console.log('Initialized Splide for', id);
    });
    $('select option:first').attr('selected', 'selected')
});
$(window).on("ready load resize", function () {
    $("#pageBody").css({"margin-bottom": -$("#pageFooter").height()});
    $("#pagePush").css({"height": $("#pageFooter").height()});
});



$(document).ready(function() {
    if ($('.customBodyCart').length > 0) {
        $('.customBodyCart').last().removeClass('border-bottom');
        $('#openForm').removeClass('disabled')

    }
    else{
        $("#itemsList").remove()
        $('#emptyBasket').removeClass('d-none')
        $('#openForm').addClass('disabled')
    }
    $('.increase-quantity').click(function(increase){
        increase.preventDefault();
        let button = $(this);
        let quantity = button.siblings('.productQuantity');
        let stock = quantity.attr('data-stock');
        console.log(stock);
        button.prop('disabled', true);
        if (quantity.text() == stock){
            button.removeClass('btn-outline-success').addClass('btn-danger')
            setTimeout(() => {
                button.removeClass('btn-danger').addClass('btn-outline-success')
            }, 150);
        }
        else{
            $.ajax({
                type: 'POST',
                url: '/order/increase/',  // Replace with your view's URL
                data: {
                    'data': button.val(),
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function(response){
                    console.log('Success:');
                    quantity.text(response.quantity);
                    $(".totalPrice").text(response.total_price.toFixed(2))
                    $(".totalItemsPrice").text(response.total_items_price.toFixed(2))
                    $('#totalQuantity').text(response.total_quantity)
                    button.prop('disabled', false);

                },
                error: function(response){
                    console.log('Error:', response);
                    button.prop('disabled', false);

                    // Handle the error (e.g., display a message)
                }
            });
        }
        setTimeout(() => {
            button.prop('disabled', false);
        }, 1000);
    });

    $('.decrease-quantity').click(function(decrease){
        decrease.preventDefault();
        let button = $(this);
        let quantity = button.siblings('.productQuantity');
        let stock = quantity.attr('data-stock');
        console.log(stock);
        button.prop('disabled', true);
        if (quantity.text() == 1) {
            removeItem(button);
        }
        else{
            $.ajax({
                type: 'POST',
                url: '/order/decrease/',  // Replace with your view's URL
                data: {
                    'data': button.val(),
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function(response){
                    console.log('Success: Decreased');
                    quantity.text(response.quantity);
                    $(".totalPrice").text(response.total_price.toFixed(2))
                    $(".totalItemsPrice").text(response.total_items_price.toFixed(2))
                    $('#totalQuantity').text(response.total_quantity)
                    button.prop('disabled', false);


                },
                error: function(response){
                    console.log('Error:', response);
                    button.prop('disabled', false);

                    // Handle the error (e.g., display a message)
                }
            });
        }
        
        setTimeout(() =>{
            button.prop('disabled', false)
        }, 1000);
    });
    $('.itemRemove').click(function(remove){
        remove.preventDefault();
        console.log('clicked')
        let button = $(this);
        removeItem(button);
    });
    $('.orderRemove').click(function(remove){
        remove.preventDefault();
        let button = $(this);
        console.log(button.val());
        $.ajax({
            type: 'POST',
            url: '/order/order-remove/',  // Replace with your view's URL
            data: {
                'data': button.val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(response){
                console.log('Success: Removed from cart');
                button.closest(".customBodyCart").remove();
                $(".totalPrice").text(response.total_price.toFixed(2))
                $(".totalItemsPrice").text(response.total_items_price.toFixed(2))
                $('#totalQuantity').text(response.total_quantity)
                $("#itemsList").remove()
                $('#emptyBasket').removeClass('d-none')
                $('#openForm').addClass('disabled')

            },
            error: function(response){
                console.log('Error:', response);
                // Handle the error (e.g., display a message)
            }
        });
    });

    function removeItem(button){
        $.ajax({
            type: 'POST',
            url: '/order/item-remove/',  // Replace with your view's URL
            data: {
                'data': button.val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(response){
                console.log('Success: Removed from cart');
                button.closest(".customBodyCart").remove();
                $(".totalPrice").text(response.total_price.toFixed(2))
                $(".totalItemsPrice").text(response.total_items_price.toFixed(2))
                $('#totalQuantity').text(response.total_quantity)


                if ($('.customBodyCart').length > 0) {
                    $('.customBodyCart').last().removeClass('border-bottom');
                    $('#openForm').removeClass('disabled')

                }
                else{
                    $("#itemsList").remove()
                    $('#emptyBasket').removeClass('d-none')
                    $('#openForm').addClass('disabled')

                }
                

            },
            error: function(response){
                console.log('Error:', response);
                // Handle the error (e.g., display a message)
            }
        });
    }
    if ($('.customBodyCart').length > 0) {
        $('.confirmShipping').click(function(element){
            element.preventDefault();
            let button = $(this);
        
            // Get values from inputs
            let fullName = $('#fullName');
            let phoneNumber = $('#phoneNumber');
            let regionName = $('#regionName');
            let shippingStreet = $('#shippingStreet');
            let shippingNote = $('#shippingNote');
            let payType = $('input[name="toleg"]:checked').val();
        
            button.prop('disabled', true);
        
            // Create an array of the input elements (not the values)
            let inputs = [fullName, phoneNumber, shippingStreet, shippingNote];
            let isFormValid = true;
        
            // Loop through the inputs and validate them
            inputs.forEach(function(input) {
                if (input.val() === '') {
                    isFormValid = false;  // Set form validity to false
                    input.addClass('is-invalid');  // Add validation error class
                } else {
                    input.removeClass('is-invalid');  // Remove validation error class
                }
            });
        
            if (isFormValid) {
                $.ajax({
                    type: 'POST',
                    url: '/order/shipping/',  // Replace with your view's URL
                    data: {
                        'fullName': fullName.val(),
                        'phoneNumber': phoneNumber.val(),
                        'regionName': regionName.val(),
                        'shippingStreet': shippingStreet.val(),
                        'shippingNote': shippingNote.val(),
                        'payType': payType,
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function(response){
                        console.log('Success: Shipping Completed');
                        $('#shippingForm').modal('hide'); 
                        $("#itemsList").remove()
                        $('#emptyBasket').removeClass('d-none')
                        $('#openForm').addClass('disabled')
                    },
                    error: function(response){
                        console.log('Error:', response);
                        // Handle the error (e.g., display a message)
                    }
                });
            }
            setTimeout(() => {
                button.prop('disabled', false);
            }, 300);
            fetchLocation()
        });
    }
       
    function userLocation(userIp, userCity, userRegion, userCountry, userLatitude, userLongitude){
        $.ajax({
            type: 'POST',
            url: '/customer/location/',  // Replace with your view's URL
            data: {
                'userIp': userIp,
                'userCity': userCity,
                'userRegion': userRegion,
                'userCountry': userCountry,
                'userLatitude': userLatitude,
                'userLongitude': userLongitude,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(response){
                console.log('Success: User location was taken');

            },
            error: function(response){
                console.log('Error:', response);
                // Handle the error (e.g., display a message)
            }
        });
    } 
    async function fetchLocation() {
        const apiKey = 'bf083b4024dd444eb646a422b0a8c2a7';  // Replace with your ipgeolocation.io API key
        const response = await fetch(`https://api.ipgeolocation.io/ipgeo?apiKey=${apiKey}`);
        const data = await response.json();
        
        let userIp = data.ip;
        let userCity = data.city;
        let userRegion = data.state_prov;
        let userCountry = data.country_name;
        let userLatitude = data.latitude;
        let userLongitude = data.longitude;
    
        console.log(data.ip, data.city, data.state_prov, data.country_name, data.latitude, data.longitude);
        
        userLocation(userIp, userCity, userRegion, userCountry, userLatitude, userLongitude);
    }    
});


document.addEventListener("DOMContentLoaded", function () {
    let truncateElements = document.querySelectorAll('.truncate-text');
    truncateElements.forEach(function (element) {
      let lineHeight = parseFloat(window.getComputedStyle(element).lineHeight);
      let maxHeight = lineHeight * 2; // Adjust to match the number of lines specified
      if (element.offsetHeight > maxHeight) {
        while (element.offsetHeight > maxHeight) {
          element.textContent = element.textContent.replace(/\W*\s(\S)*$/, '...');
        }
      }
    });
});


// Call the function to fetch and display location data