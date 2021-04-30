# Need a function that queues the next text event
# Called whenever the texting preferences are updated and when a queued event is completed

# 1 - See if the current user has a pending event queued 
    #  - if yes, delete it and go to step 2
    #  - if no, go to step 2

# 2 - Find the next event
    #  - query user
    #  - make list of day of week boolean pairs // list = ["sunday", "monday", "tuesday" ...]
    #  - get current datetime and find day of week  // offset = arrow.utcnow().format('d')
    #  - offset the list // rotate(list, offset) >>> ["thursday", "friday", "saturday" ...]
    #  - what is the next day that is true?
    #  - build a datetime using that day and the preferred time // this will be the execution_time
    #  - instantiate a text_event 