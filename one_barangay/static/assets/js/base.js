const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
        confirmButton: 'btn btn-success',
        cancelButton: 'btn btn-danger me-2'
    },
    buttonsStyling: false
})

function showSuccess(msg) {
    Swal.fire({
        icon: 'success',
        title: `Success!`,
        text: msg,
        showConfirmButton: false,
        timer: 2500
    }).then(() => {
        window.location.reload();
    });
}

function showError(error) {
    swalWithBootstrapButtons.fire({
        icon: 'error',
        title: 'Error!',
        text: `Something went wrong.<br>${error}`,
    });
}

$(document).ready(() => {
    $('[data-toggle="tooltip"]').tooltip()
})

$(() => {
    // This function gets cookie with a given name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        const {host} = document.location; // host + port
        const {protocol} = document.location;
        const sr_origin = `//${host}`;
        const origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url === origin || url.slice(0, origin.length + 1) === `${origin}/`)
            || (url === sr_origin || url.slice(0, sr_origin.length + 1) === `${sr_origin}/`)
            // or any other URL that isn't scheme relative or absolute i.e relative.
            || !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        },
    });
});