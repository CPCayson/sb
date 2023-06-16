$(document).ready(function() {
    var Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        onOpen: function(toast) {
            toast.addEventListener('mouseenter', Swal.stopTimer);
            toast.addEventListener('mouseleave', Swal.resumeTimer);
        }
    });

    $(document).ready(function() {

        var bookmarks = document.querySelectorAll('.bookmark');
        bookmarks.forEach(function(bookmark) {
            bookmark.addEventListener('click', function() {
                var fileId = bookmark.getAttribute('data-file-id');
                var hasBookmarked = bookmark.classList.contains('bookmarked');
                var url = hasBookmarked ? '/remove_bookmark/' + fileId : '/add_bookmark/' + fileId;

                fetch(url, {
                        method: 'POST'
                    })
                    .then(response => response.text())
                    .then(function() {
                        if (hasBookmarked) {
                            bookmark.classList.remove('bookmarked');
                            Toast.fire({
                                icon: 'success',
                                title: 'Bookmark removed.'
                            });
                        } else {
                            bookmark.classList.add('bookmarked');
                            Toast.fire({
                                icon: 'success',
                                title: 'Bookmark added.'
                            });
                        }
                    });
            });
        });

        var viewButtons = document.querySelectorAll(".view-btn");
        viewButtons.forEach(function(viewButton) {
            viewButton.addEventListener('click', function() {
                var fileId = viewButton.getAttribute('data-file-id');

                fetch('/generate_pdf/' + fileId)
                    .then(response => response.blob())
                    .then(blob => {
                        var fileURL = URL.createObjectURL(blob);
                        Swal.fire({
                            title: 'Embedded PDF',
                            html: '<iframe src="' + fileURL + '" width="100%" height="400px"></iframe>',
                            customClass: {
                                container: 'swal-wide'
                            },
                            showConfirmButton: true,
                            confirmButtonText: 'Thumbs Up',
                            showCancelButton: true,
                            cancelButtonText: 'Thumbs Down',
                            showDenyButton: true,
                            denyButtonText: 'Make Edits',
                        }).then((result) => {
                            if (result.isConfirmed) {
                                fetch('/like/' + fileId, {
                                        method: 'POST'
                                    })
                                    .then(response => response.text())
                                    .then(function() {
                                        Toast.fire({
                                            icon: 'success',
                                            title: 'You have upvoted this document.'
                                        });
                                    })
                                    .catch(function() {
                                        Toast.fire({
                                            icon: 'error',
                                            title: 'You have already upvoted this document.'
                                        });
                                    });
                            } else if (result.isDenied) {
                                Swal.fire({
                                    title: 'Edit Document',
                                    // Removed for brevity
                                    showConfirmButton: false,
                                    focusConfirm: false,
                                    backdrop: true,
                                    allowOutsideClick: false,
                                }).then(function() {
                                    var tabs = document.querySelectorAll('a[data-bs-toggle="pill"]');
                                    tabs.forEach(function(tab) {
                                        tab.addEventListener('shown.bs.tab', function(e) {
                                            var target = e.target.getAttribute("href");
                                            // If comments tab is active, load comments
                                            if (target === '#pills-comment') {
                                                // Use fetch to load comments from server
                                            }
                                        });
                                    });
                                });
                            } else {
                                fetch('/dislike/' + fileId, {
                                        method: 'POST'
                                    })
                                    .then(response => response.text())
                                    .then(function() {
                                        Toast.fire({
                                            icon: 'success',
                                            title: 'You have downvoted this document.'
                                        });
                                    })
                                    .catch(function() {
                                        Toast.fire({
                                            icon: 'error',
                                            title: 'You have already downvoted this document.'
                                        });
                                    });
                            }
                        });
                    }).catch(error => console.error(error));
            });
        });

        function toggleBookmark(documentId) {
            // check if the document is already bookmarked
            let isBookmarked = $(`#document-${documentId} .bookmark i`).hasClass('bookmarked');
            let url = isBookmarked ? `/remove_bookmark/${documentId}` : `/add_bookmark/${documentId}`;
            $.post(url, function(data) {
                // toggle the 'bookmarked' class
                $(`#document-${documentId} .bookmark i`).toggleClass('bookmarked');
            }).fail(function() {
                alert('An error occurred. Please try again.');
            });
        }

        function likeDocument(documentId) {
            $.post(`/like/${documentId}`, function(data) {
                // increment the like count or change the like button state
            }).fail(function() {
                alert('An error occurred. Please try again.');
            });
        }

        function dislikeDocument(documentId) {
            $.post(`/dislike/${documentId}`, function(data) {
                // increment the dislike count or change the dislike button state
            }).fail(function() {
                alert('An error occurred. Please try again.');
            });
        }
    })
});