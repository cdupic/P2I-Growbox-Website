function filterNotifications() {
    var filter = document.getElementById('typeFilter').value;
    var notifications = document.getElementsByClassName('notification');

    for (var i = 0; i < notifications.length; i++) {
        var notification = notifications[i];
        if (filter === 'all' || notification.getAttribute('data-type') === filter) {
            notification.style.display = 'flex';
        } else {
            notification.style.display = 'none';
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var DateTime = luxon.DateTime;
    var notifications = document.getElementsByClassName('notification-date');

    for (var i = 0; i < notifications.length; i++) {
        var dateElement = notifications[i];
        var date = dateElement.getAttribute('data-date');
        var formattedDate = DateTime.fromSQL(date, {zone: 'utc'}).setLocale('fr').toFormat('dd MMMM yyyy - HH:mm');
        dateElement.textContent = formattedDate;
    }
});
