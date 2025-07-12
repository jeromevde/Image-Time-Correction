-- EXIF Datetime Updater - AppleScript for Automator Service
-- This script is used in the Automator Quick Action

on run {input, parameters}
    -- Get the path to the shell script
    set scriptPath to (path to me as text) & "Contents:Resources:exif_datetime_service.sh"
    
    -- Convert file paths to POSIX paths
    set posixPaths to {}
    repeat with anItem in input
        set end of posixPaths to POSIX path of anItem
    end repeat
    
    -- Build the command
    set shellCommand to "bash " & quoted form of POSIX path of scriptPath
    repeat with aPath in posixPaths
        set shellCommand to shellCommand & " " & quoted form of aPath
    end repeat
    
    -- Execute the command
    try
        do shell script shellCommand
    on error errorMessage
        display dialog "Error running EXIF Datetime Updater: " & errorMessage buttons {"OK"} default button "OK"
    end try
    
    return input
end run
