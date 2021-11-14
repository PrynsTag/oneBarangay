$.getScript("https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
    .done(function (script, textStatus) {
        google.maps.event.addDomListener(window, "load", initAutoComplete)
    })


let autocomplete;

function initAutoComplete() {
    const circle = new google.maps.Circle({
        center: {lat: 14.715960890875737, lng: 120.95388332850888},
        radius: 3000
    });

    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id-google-address'),
        {
            types: ['geocode'],
            //default in this app is "PH"
            componentRestrictions: {'country': ['ph']},
            bounds: circle.getBounds(),
            strictBounds: true
        })

    autocomplete.addListener('place_changed', onPlaceChanged);
}


function onPlaceChanged() {

    const place = autocomplete.getPlace();
    console.log(place)
    const geocoder = new google.maps.Geocoder();
    const address = document.getElementById('id-google-address').value;

    geocoder.geocode({'address': address}, function (results, status) {

        if (status === google.maps.GeocoderStatus.OK) {
            const latitude = results[0].geometry.location.lat();
            const longitude = results[0].geometry.location.lng();

            $('#id_longitude').val(longitude)
            $('#id_latitude').val(latitude)
        }
    });

    if (!place.geometry) {
        document.getElementById('id-google-address').placeholder = "*Begin typing address";
    } else {
        let street_number;
        let route;
        for (let i = 0; i < place.address_components.length; i++) {
            for (let j = 0; j < place.address_components[i].types.length; j++) {
                if (place.address_components[i].types[j] === "street_number") {
                    street_number = place.address_components[i].long_name
                }
                if (place.address_components[i].types[j] === "route") {
                    route = place.address_components[i].long_name
                }
                if (place.address_components[i].types[j] === "locality") {
                    $('#id_city').val(place.address_components[i].long_name)
                }
                if (place.address_components[i].types[j] === "administrative_area_level_1") {
                    $('#id_region').val(place.address_components[i].short_name)
                }
                if (place.address_components[i].types[j] === "administrative_area_level_2") {
                    $('#id_province').val(place.address_components[i].long_name)
                }
                if (place.address_components[i].types[j] === "country") {
                    $('#id_country').val(place.address_components[i].long_name)
                }

                if (place.address_components[i].types[j] === "postal_code") {
                    $('#id_zip_code').val(place.address_components[i].long_name)
                }
            }
        }
        $('#id_street').val(`${street_number ? `${street_number} ` : ''}${route}`)

        //find all hidden inputs & ignore csrf token
        const x = $("input:hidden");
        const hidden_fields = ["csrfmiddlewaretoken", "country", "latitude", "longitude"];

        for (let i = 0; i < x.length; i++) {
            const field_name = x[i].name;
            if (!(hidden_fields.includes(field_name)))
                x[i].type = "text";

            x.eq(x).attr("class", 'hidden-el')

            $("label[for='" + x[i].id + "']").removeAttr('hidden');
            $(`${x[i].id}`).hide().fadeIn(400);
        }

        //fade in the completed form
        // FIXME: Doesn't fade
        $('.hidden-el').hide().fadeIn(400);

        const $submitBtn = $('#submit-btn')
        const $resetBtn = $('#reset-btn')
        const $googleAddress = $('#id-google-address')

        $submitBtn.removeAttr("hidden").hide().fadeIn(400)
        $resetBtn.removeAttr("hidden").hide().fadeIn(400)
        $resetBtn.on('click', () => {
            $('#setup-form').trigger("reset");
        })

        $googleAddress.hide()
        $googleAddress.removeAttr('required')
        $('#id_address').attr('required')
        $("label[for='id-google-address']").hide()
    }
}