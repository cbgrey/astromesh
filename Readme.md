
_getConfig_

     { value:null }
Initiates a request to get the current droid control configuration. Droid will return a “configuration” event. There is no data value. 


_drive_

     {
          “direction”:int,
           “velocity”: int
     }

Direction and Velocity are each values between -255 and +255. These values will be translated by the droid into Left/Right foot motor pulse values. 

rotateDome


     {
          “value”:int
     }

Rotates the dome. Value of -255 to +255 will change direction and speed. 

changeDisplay
Changes various display modes on the droid. 

{
     “display”:displayName,
     “mode”: modename,
     “displayText”: text
}

displayName = “fld1”,”fld2”,”rld” or “all” etc. 
modeName = “random” or some other pre-defined name. 
displayText = Text to display if mode supports it. 


playSound
Plays a sound or sound playlist on the droid. 

{
     “type”:soundType,
     “name”:soundName
}

type: either ‘single’ or ‘playlist’
name: the name of the file or playlist


changeLegMode

Changes the leg orientation of the droid for those that support a 2-3-2 configuration. 

{
     “mode”:modeName
}

modeName = “2leg” or “3leg”


changePanels
Changes open/closed state of dome panels. 
{
     “pp1”:panelState,
     “pp4”: panelState
}

panelState = int of 0 to 100 that indicates full closed or full open. 


custom
Available to send custom commands for any unimplemented events. Expansion for droidbuilder to use. 
{
     ‘data’:customData
}