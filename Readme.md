![](./astromesh_logo.png "Optional title")


### Purpose and Overview

Astromesh was imagined to be a "glue" solution for builders of Astromech and
similar droids. As a builder I noted that each control or interface solution sat
on an island with no universal set of tools or protocols to bind them. It was
also intended to create a more modern control stack vs the typical use of RC
controllers  with secondary controllers for items like lights and sounds. The hope is to help evolution of user interface and controller options by defining a standardized controller <-> droid API. 

The project has a secondary goal to provide software-only solutions wherever possible. It would be ideal to be able to build an entire command and control stack purely out of "off the shelf" components. While customized hardware offers some great advantages it is somtimes difficult to obtain or challenging to contruct. Astromesh will attempt to define a standardized platform that could be constructed from commodity parts. 

###### Summarized project objectives:

* Provide a performant, bi-directional, event-driven central control server. 
* The stack should be able to be run on a range of hardware from very small and cheap to very powerful. 
* Define a standardized control API to allow interface developers freedom of expression without having to create the entire "stack".
* Provide a simple, usable control interface for Android and/or iOS devices. 
* Provide a simple droid simulation view. 
* Implement necessary safeguards for use in "the real world". Can't have a droid running off into a crowd of fans. 
* Define a standardized "driver" protocol for future expandability (eg: different lighting systems could be controlled by a standardized set of commands.) 
* Provide a protocol for droid "self-description". This will allow controllers to query a droid for its supported devices and sounds. 


### Technologies



### Device List
One of the objectives of the project is to standardize or codify a typical set of Astromech devices and control points. 

Currently:

- Drive System (L/R motors)
- 2-3-2 Servos (quantify)
- Dome Rotation
- Holoprojectors (motion)
     - HP1
     - HP2
     - HP3
- Pie Panels
     * PP1
     * PP2
     * PP3
     * PP4
     * PP5
- Dome Top
- Side Panels
     * SP1
     * SP2
     * SP3
     * SP4
     * SP5
     * SP6# 
- Display Systems Lights
     - Teeces Controller
     - JEDI Controller
     - Magic Panel

- Sound Player

- Sensors/Telemetry
     - Temperature
     - GPS
     - Battery Levels
     - Runtime
     - Video stream 
     - etc


### Control Protocol Event Types

     * Controller Commands
          - getConfig
          - drive
          - rotateDome
          - changeDisplay
               * displayID (RLD, FLD1, FLD2 etc)
               * displayMode
          - playSound
          - change232
          - changeHP
          - changePanel
          - changeLFS
          - changePeriscope
          - customCommand
               * [a placeholder for custom commands not defined in the spec]

     * Droid Events
          - configuration
               * [description of available droid-ware]
          - status
               * batteryLevels
               * gpsLocation
               * runtime
               * temp



### Control Protocol Specifications - Commands

##### getConfig

     { value:null }
Initiates a request to get the current droid control configuration. Droid will return a “configuration” event. There is no data value. 


##### drive
Drives the droid via the left and right foot motors.

     {
          “direction”:int,
           “velocity”: int
     }

Direction and Velocity are each values between -255 and +255. These values will be translated by the droid into Left/Right foot motor pulse values. 

##### rotateDome
Rotates the dome. Value of -255 to +255 will change direction and speed. 

     {
          “value”:int
     }



##### changeDisplay
Changes various display modes on the droid. 

     {
          “display”:displayName,
          “mode”: modename,
          “displayText”: text
     }

displayName = “fld1”,”fld2”,”rld” or “all” etc. 
modeName = “random” or some other pre-defined name. 
displayText = Text to display if mode supports it. 


##### playSound
Plays a sound or sound playlist on the droid. 

     {
          “type”:soundType,
          “name”:soundName
     }

type: either ‘single’ or ‘playlist’
name: the name of the file or playlist


##### changeLegMode

Changes the leg orientation of the droid for those that support a 2-3-2 configuration. 

     {
          “mode”:modeName
     }

modeName = “2leg” or “3leg”


##### changePanels
Changes open/closed state of dome panels. 

     {
          “pp1”:panelState,
          “pp4”: panelState
     }

panelState = int of 0 to 100 that indicates full closed or full open. 


##### custom
Available to send custom commands for any unimplemented events. Expansion for droidbuilder to use. 

     {
          ‘data’:customData
     }


