Routes:

    User
        /users/<int:user_id>: GET, POST, PUT, DELETE for individual users.
        /users: GET for all users.

    Document
        /documents/<int:document_id>: GET, POST, PUT, DELETE for individual documents.
        /documents: GET for all documents.
        /documents/user/<int:user_id>: GET for all documents of a specific user.

    Subscription
        /subscriptions/<int:subscription_id>: GET, POST, PUT, DELETE for individual subscriptions.
        /subscriptions: GET for all subscriptions.
        /subscriptions/user/<int:user_id>: GET for all subscriptions of a specific user.

    School
        /schools/<int:school_id>: GET, POST, PUT, DELETE for individual schools.
        /schools: GET for all schools.
        /schools/documents/<int:school_id>: GET for all documents of a specific school.

    Comment
        /comments/<int:comment_id>: GET, POST, PUT, DELETE for individual comments.
        /comments/document/<int:document_id>: GET for all comments of a specific document.

    Like
        /likes/<int:like_id>: GET, POST, DELETE for individual likes.
        /likes/document/<int:document_id>: GET for all likes of a specific document.

    Dislike
        /dislikes/<int:dislike_id>: GET, POST, DELETE for individual dislikes.
        /dislikes/document/<int:document_id>: GET for all dislikes of a specific document.

    SuggestedEdit
        /suggested_edits/<int:suggested_edit_id>: GET, POST, PUT, DELETE for individual suggested edits.
        /suggested_edits/document/<int:document_id>: GET for all suggested edits of a specific document.

    Bookmark
        /bookmarks/user/<int:user_id>: GET, POST, DELETE for all bookmarks of a specific user.
        /bookmarks/document/<int:document_id>: GET for all users who bookmarked a specific document.

Models and their capabilities:

    User
        CRUD (Create, Retrieve, Update, Delete) operations on User instances.
        Relationship with Document (documents, bookmarked_files), Subscription (subscriptions).

    Document
        CRUD operations on Document instances.
        Relationship with User (user), Comment (comments), Like (likes), Dislike (dislikes), SuggestedEdit (suggested_edits), School (school).

    Subscription
        CRUD operations on Subscription instances.
        Relationship with User (user).

    School
        CRUD operations on School instances.
        Relationship with Document (documents).

    Comment
        CRUD operations on Comment instances.
        Relationship with User (user), Document (document).

    Like
        CRUD operations on Like instances.
        Relationship with User (user), Document (document).

    Dislike
        CRUD operations on Dislike instances.
        Relationship with User (user), Document (document).

    SuggestedEdit
        CRUD operations on SuggestedEdit instances.
        Relationship with User (user), Document (document).

    Bookmark
        CRUD operations on Bookmarks instances (association table).
        Relationship with User, Document
        
        
Ok I have  a grid layout of  article  cards, that have the thumbnail of a png image and below have organized informatiom - have name of document, subject, school, date posted,  a bookmark option (seen as an icon). Each article is uploaded by a user who uploads, an exam and inputs these fields, the pdf is saved in a folder as well as a png image of the pdf to be used as the picture icon of the article card. The textfeilds (i.e., name of document, subject, school,) are wiggle buttons, where if one is clicked on, the card flips over and displays a user generated edit suggetsion based on rank. If the front of the article is clicked on a accordian is open that has additional options, like a document viewer, a like button, dislike buttun, information about the article, and a comments section. Rules: With ranking users can only have one vote, however if they click on the opposite button (like the dislike instead of the like, the tally off the vote will bring down the like vote by user by 0 and add +=1 to the dislike). Bookmarks are toggled. If clicked a bookmark is saved with the user where he can view in his profile, if unclicked that bookmark is deleted. When a wiggle button is clicked (for either subject, professor, school) the card flips over and a ranking system form is displayed that is only targeted to the selected clicked wiggle button - bject has its own ranking system, professor has its own ranking sytem, etc) - literally its  snippet representing a leaderboard. It consists of a header with a title and a share button, followed by a leaderboard table with rankings, names, and points-. If the ranking of a suggested edit from a user is ranked higher then the default, a crud option is performed and that name now becomes the name of the selected.  The Document viewer has a zoom, resize, download ETC OPTIONS, and the comment section is a reddit like comment box for users -  a comments section with Bootstrap styling. It includes a structure for displaying comments and replies, along with buttons for upvoting, downvoting, and replying to comments. There is also JavaScript code that adds functionality to dynamically generate reply input fields and handle submission of replies.- to answerquestions and get comments on each of the exams' questions and answers.  Users can not edit their already posted answers but may delete them.  


If an article has three times more negative likes then positive, it is deleted from the database. 