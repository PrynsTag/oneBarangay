if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/firebase-messaging-sw.js').then(() => {
      // Registration was successful
    }, () => {
      // registration failed :(
    });
  });
}
let uid;
auth.onAuthStateChanged((user) => {
  if (user) {
    uid = user.uid;
  } else {
    // console.log('User not logged in.');
  }
});

// eslint-disable-next-line no-unused-vars
function subscribeUser(platform) {
  Notification.requestPermission().then((permission) => {
    if (permission === 'granted') {
      messaging.getToken({ vapidKey: 'BHmD1lh0dF-eHLfDMOAeQq8u82l2VWekyWSum1VW-nh4yQRd-iewUEVY0qL-zXsl1bO-_N6Y0vZP72ph0GFWioM' }).then((currentToken) => {
        if (currentToken) {
          if (uid) {
            const docRef = firestore_db.collection('users').doc(uid);
            docRef.get().then((doc) => {
              if (doc.exists) {
                docRef.set({ [platform]: currentToken }, { merge: true });
              } else {
                // doc.data() will be undefined in this case
                // console.log('No such document!');
              }
            }).catch(() => {
              // console.log('Error getting document:', error);
            });
          }
        } else {
          // console.log('No registration token available. Request permission to generate one.');
        }
      }).catch(() => {
        // console.log('An error occurred while retrieving token. ', err);
      });
    }
  });
}

// eslint-disable-next-line no-unused-vars
function unSubscribeUser(platform) {
  // Notification.permission = 'denied';
  const docRef = firestore_db.collection('users').doc(uid);
  docRef.update({ [platform]: '' });
}

messaging.onMessage((payload) => {
  const notificationTitle = `[FG]${payload.data.title}`;
  const notificationOptions = {
    body: payload.data.body,
    icon: payload.data.icon,
    requireInteraction: payload.data.requireInteraction,
  };

  if (!('Notification' in window)) {
    alert('This browser does not support system notifications');
  }
  // Let's check whether notification permissions have already been granted
  else if (Notification.permission === 'granted') {
    // If it's okay let's create a notification
    try {
      const notification = new Notification(notificationTitle, notificationOptions);
      notification.onclick = (event) => {
        event.preventDefault(); // prevent the browser from focusing the Notification's tab
        window.open(payload.data.tag, '_blank');
        notification.close();
      };
    } catch (err) {
      try { // Need this part as on Android we can only display notifications thru the serviceworker
        navigator.serviceWorker.ready.then((registration) => {
          registration.showNotification(notificationTitle, notificationOptions);
        });
      } catch (err1) {
        alert(err1.message);
      }
    }
  }
});

const swalWithBootstrapButtons = Swal.mixin({
  customClass: {
    confirmButton: 'btn btn-success',
    cancelButton: 'btn btn-danger me-2',
  },
  buttonsStyling: false,
});

function showSuccess(msg) {
  Swal.fire({
    icon: 'success',
    title: 'Success!',
    text: msg,
    showConfirmButton: false,
    timer: 3000,
  });
}

function showError(error) {
  swalWithBootstrapButtons.fire({
    icon: 'error',
    title: 'Error!',
    text: `Something went wrong.<br>${error}`,
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i += 1) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function sendToServer(url, msg) {
  $.ajax({
    url,
    type: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    success: () => {
      showSuccess(msg);
    },
    error: (errorThrown) => {
      showError(errorThrown);
    },
  });
}

$(document).ready(() => {
  $('[data-toggle="tooltip"]').tooltip();
});

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
    const { host } = document.location; // host + port
    const { protocol } = document.location;
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
