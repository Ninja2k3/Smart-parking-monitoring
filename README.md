# Smart-parking-monitoring (MCES EL)
Kushal J - 1RV21CS072
Niranjan S - 1RV21CS103
Mohammad Afzal - 1RV21CS91
Nandan Kumar HR - 1RV21CS97

Software approach with openCV :
Webapp made with flask and mongoDB, features real time monitoring of parking slots with ESP32 sensor and image processing with openCV. Sensor data is transmitted to firebase realtime database.

For detection of vehicles in parking spots, open source repository PARKING SPACE DETECTION IN OPENCV by olgarose was referred. The user had created a method of detecting cars with computer vision. Firstly a local video file and a screenshot of one of its frames are passed as input. User is allowed to declare coordinates on the image for parking lot by letting them use their mouse as a brush. 
The approach for this was using an openCV window where the mouse can give inputs. The stored coordinates were converted to yaml data which was then parsed to form quadrilaterals around the given coordinates for the specified parking area. Filters like Gaussian blur and canny detection allow for monitoring for the presence of vehicles in the declared parking spot by marking them with green.
Output is again displayed in an openCV window.

To make this work with our preferred tech stack we made a few changes :
We understood the code structure and the functions used, we used the coordinates generator strictly to give input and we are treating this a seperate software only available to the admin of our website. feeder.py file allows us to generate coordinates for monitoring. In the motiondetecter.py file we had to accomodate streaming the monitoring video footage to our website and not through an openCV window.
We accomplished this by using the imencode file inbuilt in openCV. We encoded each frame of the video in '.jpg' format, added it to a buffer and streamed bytewise to our server in a way that our flask server could convniently stream the video file without delay. Lot of modifications had to be done in the coordinatesgenerator and motiondetector files. Motion detector  function was set to be called on the click of a button in our website.
'coordinates_1.y' in the project is an example for a file which stores the coordinates. We can pass the preferred coordinates file as an argument to our function. We changed the code to store the marked coordinates until we explicitly decide to change it again by running the feeder.py file.

In summary,

run feeder.py in api folder to pick coordinates

run the flask server

register and login to site

click on the park button to view monitored video footage
