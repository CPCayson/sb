function fetchComments() {
    var documentId = {
        { document.id | tojson } };
    $.ajax({
        url: '/comments/document/' + documentId,
        type: 'GET',
        success: function(response) {
            $('#comment-section').html(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

// Function to submit a new comment using AJAX
function submitComment(event) {
    event.preventDefault();
    var commentContent = $('#new-comment').val();
    var documentId = {
        { document.id } };

    $.ajax({
        url: '/comments/document/' + documentId,
        type: 'POST',
        data: { content: commentContent },
        success: function(response) {
            fetchComments(); // Fetch and update the comments after submitting a new comment
            $('#new-comment').val('');
        },
        error: function(error) {
            console.log(error);
        }
    });
}

// Add event listener to the comment form submit button
$('#add-comment').on('click', submitComment);

// Function to handle AJAX requests for upvoting a comment
function likeComment(commentId) {
    $.ajax({
        url: '/comments/' + commentId + '/like',
        type: 'POST',
        success: function(response) {
            // Update the upvote count in the specific comment
            $('#comment-' + commentId + ' .upvote-count').text(response.upvotes);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

// Add event listener to the upvote buttons
$('.upvote-btn').on('click', function() {
    var commentId = $(this).data('comment-id');
    likeComment(commentId);
});

// Function to handle AJAX requests for downvoting a comment
function dislikeComment(commentId) {
    $.ajax({
        url: '/comments/' + commentId + '/dislike',
        type: 'POST',
        success: function(response) {
            // Update the downvote count in the specific comment
            $('#comment-' + commentId + ' .downvote-count').text(response.downvotes);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

// Add event listener to the downvote buttons
$('.downvote-btn').on('click', function() {
    var commentId = $(this).data('comment-id');
    dislikeComment(commentId);
});

// Fetch the comments on page load
fetchComments();