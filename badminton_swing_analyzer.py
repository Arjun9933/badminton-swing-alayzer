import cv2
import mediapipe as mp
import math
import numpy as np
import time

print("=== Badminton Swing Analyzer ===")
handedness = input("Are you left-handed or right-handed? (enter 'left' or 'right'): ").strip().lower()

if handedness == 'left':
    print("Loading left-handed swing analyzer...")
    #base options
    base_options = mp.tasks.BaseOptions(model_asset_path = "pose_landmarker_full.task")
    #choose options and running mdoe
    options = mp.tasks.vision.PoseLandmarkerOptions(base_options = base_options, running_mode = mp.tasks.vision.RunningMode.VIDEO)
    #create detector
    detector = mp.tasks.vision.PoseLandmarker.create_from_options(options)




    # angle func
    def angle_calc(point_a, point_b, point_c, w, h):
        angle1 = math.atan2((point_a.y - point_b.y) * h, (point_a.x - point_b.x) * w)

        angle2 = math.atan2((point_c.y - point_b.y) * h, (point_c.x - point_b.x) * w)

        angle = math.degrees(angle1-angle2)

        abs_angle = abs(angle)

        if abs_angle > 180:
            abs_angle = 360 - abs_angle

        angle1 = math.degrees(angle1)
        angle2 = math.degrees(angle2)

        return abs_angle, angle1, angle2




    elbow_farther_ear_horizontally_done = False
    shoulders_rotated_done = False
    pos_3_angle_check = False
    avg_values_calibration = False
    elbow_height_check = []
    angle_2_list = []
    shoulder_width_values = []
    hip_width_values = []

    video = "Put your video path here"
    cap = cv2.VideoCapture(video)

    while cap.isOpened():



        bool,frame = cap.read()

        if not bool:
            break

    #change from brg 2 rgb
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #proper frame
        mediapipe_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    #ask cv what time it is rn in milloseconds
        frame_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
    #mediapipe analyses the frame and needs the time per frame and stuff and detects it
        result = detector.detect_for_video(mediapipe_frame, frame_time)

        if result and result.pose_landmarks:
            
            player = result.pose_landmarks[0]

            left_shoulder = player[11]
            right_shoulder = player[12]
            left_hip = player[23]
            right_hip = player[24]
            left_elbow = player[13]
            left_wrist = player[15]
            left_ear = player[7]
            nose = player[0]


            wrist_above_shoulder = left_wrist.y < right_shoulder.y
            #angle_greater_than_105 = abs_angle > 105
            elbow_lower_equal_shoulder = left_elbow.y + 0.1 >= right_shoulder.y

            h, w, _ = frame.shape


            #angle
            abs_angle, angle1, angle2 = angle_calc(left_wrist, left_elbow, right_shoulder, w, h)




            
            current_pose = None

            #pose identification
            pose_none = None
            pose2 =  left_wrist.y < right_shoulder.y and abs_angle < 105 and not left_elbow.y + 0.1 >= right_shoulder.y
            pose3 = abs_angle > 110

            
            if pose2:
                current_pose = pose2
                
            elif pose3:
                current_pose = pose3
            else:
                current_pose = pose_none
            

            #print(f"angle is{abs_angle}")
            if current_pose == pose3:
                if 110 < angle2 < 130:
                    angle_2_list.append("g") # g is for "good"
                else:
                    angle_2_list.append("b") # b is for "bad"
                



            shoulder_width = (left_shoulder.x) - (right_shoulder.x)
            
            hip_width = (left_hip.x) - (right_hip.x)
            




            left_right_z_shoulder_difference = left_shoulder.z - right_shoulder.z
            left_right_z_hip_difference = right_hip.z - left_hip.z

            
            

    #here to make sure avg values aren't re calculatied again and again to help optimize code.
            if not avg_values_calibration:
                #checks if shoulder and hips are completely straight before recording thier values.
                if abs(left_right_z_hip_difference) < 0.15 and abs(left_right_z_shoulder_difference) < 0.15:
                
                
                    if len(shoulder_width_values) < 30:
                        shoulder_width_values.append(shoulder_width)
                        avg_shoulder_width_values = sum(shoulder_width_values) / len(shoulder_width_values)
                    
                
                
                        
                
                    if len(hip_width_values) < 30:
                        hip_width_values.append(hip_width)
                        avg_hip_width_values = sum(hip_width_values) / len(hip_width_values)
                    
                
        
                    if len(hip_width_values) and len(shoulder_width_values) == 30:
                        avg_values_calibration = True

                
                    
                    
        


            #shoulder rotation check used in pos 3 and pos 2
            shoulders_rotated = shoulder_width < (avg_shoulder_width_values * 0.0375)
            
            # create checks for the elbow and ear to be used in position 2

            elbow_above_ear_vertically = left_elbow.y < (left_ear.y - (-0.055 * h))
            elbow_farther_ear_horizontally = left_elbow.x < left_ear.x
            wrist_behind_ear = left_ear.x > left_wrist.x

            
            if current_pose == pose2:
                print("2")
            elif current_pose == pose3:
                print("3")
            else:
                print("none")



    #pose2 checks
            if current_pose == pose2:
                if elbow_above_ear_vertically:
                    elbow_height_check.append("g") # g for good
                else:
                    elbow_height_check.append("b") # b for bad
                        
                if not elbow_farther_ear_horizontally_done:
                    if elbow_farther_ear_horizontally:
                        elbow_farther_ear_horizontally_done = True


            if current_pose == pose3:
                if not pos_3_angle_check:
                        if abs_angle > 140:
                            pos_3_angle_check = True

            if shoulders_rotated_done == False:
                        if shoulders_rotated:
                            shoulders_rotated_done = True
            
                        


            print(avg_shoulder_width_values)
            print(shoulder_width)
            
    #map point and lines onto the body
            right_shoulder_point = (int(right_shoulder.x * w), int(right_shoulder.y * h))
            left_shoulder_point  = (int(left_shoulder.x * w), int(left_shoulder.y * h))

            left_hip_point = (int(left_hip.x * w), int(left_hip.y * h))
            right_hip_point = (int(right_hip.x * w), int(right_hip.y * h))

            left_ear_point = (int(left_ear.x * w), int((left_ear.y - 0.055) * h))


            left_elbow_point = (int(left_elbow.x * w),int(left_elbow.y * h))

            left_wrist_point = (int(left_wrist.x * w),int((left_wrist.y) * h))

            # check visibility not being used as of the moment
            visibility_True = (right_shoulder.visibility > 0.6 and left_elbow.visibility > 0.6 and left_wrist.visibility > 0.6)

            if visibility_True:
                cv2.circle(frame, right_shoulder_point, 4, (0,0,255), -1)
                cv2.circle(frame, left_elbow_point, 4, (0,0,255), -1)
                cv2.circle(frame, left_wrist_point, 4, (0,0,255), -1)
                cv2.circle(frame, left_shoulder_point, 4, (0,0,255), -1)
                cv2.circle(frame, left_hip_point, 4, (0,0,255), -1)
                cv2.circle(frame, right_hip_point, 4, (0,0,255), -1)
                cv2.circle(frame, left_ear_point, 4, (0,0,255), -1)
                
                #line up the circles

                cv2.line(frame, left_shoulder_point, left_elbow_point, (255,0,0), 2)
                cv2.line(frame, left_elbow_point, left_wrist_point, (255,0,0), 2)
                cv2.line(frame, right_shoulder_point, left_shoulder_point, (255,0,0), 2)
                cv2.line(frame, right_hip_point, left_hip_point, (255,0,0), 2)

                # cv2.putText(frame,f"elbow to wrist: {angle1:.1f}", (right_wrist_point), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                # cv2.putText(frame, f"elbow to wrist: {angle2:.1f}", (right_shoulder_point), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)





        cv2.imshow("pic",frame)

        if cv2.waitKey(1) == ord("q"):
            break


#final checks and prints
    if angle_2_list.count("g") >= 2:
        print("good elbow placement on the final swing good contact point")
    else:
        print("bad contact point, have elbow facing the celing to get a higher contact point")

    if elbow_height_check.count("g") >= 4:
        print("good elbow height and position during swing")
    else:
        print("during swing elbow has to be positioned higher, facing the ceiling (not all the way).")

    if not elbow_farther_ear_horizontally_done:
        ("elbow must be farther than the ear")

    if shoulders_rotated_done == True:
        print("good body rotation")
    else:
        print("you need to rotate your shoulders and hips all the way during your swing")


    if not pos_3_angle_check:
        print("you need a higher contact point")


    print(elbow_height_check)
    print(angle_2_list)


    cap.release()
    cv2.destroyAllWindows()


elif handedness == 'right':
    print("Loading right-handed swing analyzer...")
        #base options
    base_options = mp.tasks.BaseOptions(model_asset_path = "pose_landmarker_full.task")
    #choose options and running mode
    options = mp.tasks.vision.PoseLandmarkerOptions(base_options = base_options, running_mode = mp.tasks.vision.RunningMode.VIDEO)
    #create detector
    detector = mp.tasks.vision.PoseLandmarker.create_from_options(options)




    # angle func
    def angle_calc(point_a, point_b, point_c, w, h):
        angle1 = math.atan2((point_a.y - point_b.y) * h, (point_a.x - point_b.x) * w)

        angle2 = math.atan2((point_c.y - point_b.y) * h, (point_c.x - point_b.x) * w)

        angle = math.degrees(angle1-angle2)

        abs_angle = abs(angle)

        if abs_angle > 180:
            abs_angle = 360 - abs_angle

        angle1 = math.degrees(angle1)
        angle2 = math.degrees(angle2)

        return abs_angle, angle1, angle2




    elbow_farther_ear_horizontally_done = False
    shoulders_rotated_done = False
    pos_3_angle_check = False
    avg_values_calibration = False
    elbow_height_check = []
    angle_2_list = []
    shoulder_width_values = []
    hip_width_values = []

    video = "put your video path here"
    cap = cv2.VideoCapture(video)

    while cap.isOpened():



        bool,frame = cap.read()

        if not bool:
            break

    #change from brg 2 rgb
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #proper frame
        mediapipe_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    #ask cv what time it is rn in milloseconds
        frame_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
    #mediapipe analyses the frame and needs the time per frame and stuff and detects it
        result = detector.detect_for_video(mediapipe_frame, frame_time)

        if result and result.pose_landmarks:
            
            player = result.pose_landmarks[0]

            left_shoulder = player[11]
            right_shoulder = player[12]
            left_hip = player[23]
            right_hip = player[24]
            right_elbow = player[14]
            right_wrist = player[16]
            right_ear = player[8]
            nose = player[0]


            wrist_above_shoulder = right_wrist.y < right_shoulder.y
            #angle_greater_than_105 = abs_angle > 105
            elbow_lower_equal_shoulder = right_elbow.y + 0.1 >= right_shoulder.y

            h, w, _ = frame.shape


            #angle
            abs_angle, angle1, angle2 = angle_calc(right_wrist, right_elbow, right_shoulder, w, h)




            
            current_pose = None

            #pose identification
            pose_none = None
            pose2 =  right_wrist.y < right_shoulder.y and abs_angle < 105 and not right_elbow.y + 0.1 >= right_shoulder.y
            pose3 = abs_angle > 110

            
            if pose2:
                current_pose = pose2
                
            elif pose3:
                current_pose = pose3
            else:
                current_pose = pose_none
            

            #print(f"angle is{abs_angle}")
            if current_pose == pose3:
                if 110 < angle2 < 130:
                    angle_2_list.append("g") # g is for "good"
                else:
                    angle_2_list.append("b") # b is for "bad"
                



            shoulder_width = (left_shoulder.x) - (right_shoulder.x)
            
            hip_width = (left_hip.x) - (right_hip.x)
            




            left_right_z_shoulder_difference = left_shoulder.z - right_shoulder.z
            left_right_z_hip_difference = right_hip.z - left_hip.z

    #here to make sure avg values aren't re calculatied again and again to help optimize code.
            if not avg_values_calibration:
                #checks if shoulder and hips are completely straight before recording thier values.
                if abs(left_right_z_hip_difference) < 0.15 and abs(left_right_z_shoulder_difference) < 0.15:
                
                
                    if len(shoulder_width_values) < 30:
                        shoulder_width_values.append(shoulder_width)
                        avg_shoulder_width_values = sum(shoulder_width_values) / len(shoulder_width_values)
                    
                
                
                        
                
                    if len(hip_width_values) < 30:
                        hip_width_values.append(hip_width)
                        avg_hip_width_values = sum(hip_width_values) / len(hip_width_values)
                    
                
        
                    if hip_width_values and shoulder_width_values == 30:
                        avg_values_calibration = True

                
                    
                    
        


            #shoulder rotation check used in pos 3 and pos 2
            shoulders_rotated = shoulder_width < avg_shoulder_width_values * 0.0375
            
            # create checks for the elbow and ear to be used in position 2

            elbow_above_ear_vertically = (right_elbow.y * h) < ((right_ear.y - 0.055) * h)
            elbow_farther_ear_horizontally = right_elbow.x > right_ear.x
            wrist_behind_ear = right_ear.x > right_wrist.x

            
            if current_pose == pose2:
                print("2")
            elif current_pose == pose3:
                print("3")
            else:
                print("none")



    #pose2 checks
            if current_pose == pose2:
                if elbow_above_ear_vertically:
                    elbow_height_check.append("g") # g for good
                else:
                    elbow_height_check.append("b") # b for bad
                        
                if not elbow_farther_ear_horizontally_done:
                    if elbow_farther_ear_horizontally:
                        elbow_farther_ear_horizontally_done = True



            if current_pose == pose3:
                if not pos_3_angle_check:
                        if abs_angle > 140:
                            pos_3_angle_check = True

            if shoulders_rotated_done == False:
                            if shoulders_rotated:
                                shoulders_rotated_done = True
                        

            print(f"avg shoulder values are {avg_shoulder_width_values}")
            print(f"current shoulder width is {shoulder_width}")


            
    #map point and lines onto the body
            right_shoulder_point = (int(right_shoulder.x * w), int(right_shoulder.y * h))
            left_shoulder_point  = (int(left_shoulder.x * w), int(left_shoulder.y * h))

            left_hip_point = (int(left_hip.x * w), int(left_hip.y * h))
            right_hip_point = (int(right_hip.x * w), int(right_hip.y * h))

            right_ear_point = (int(right_ear.x * w), int((right_ear.y - 0.055) * h))


            elbow_point = (int(right_elbow.x * w),int(right_elbow.y * h))

            right_wrist_point = (int(right_wrist.x * w),int((right_wrist.y) * h))

            # check visibility not being used as of the moment
            visibility_True = (right_shoulder.visibility > 0.6 and right_elbow.visibility > 0.6 and right_wrist.visibility > 0.6)

            if visibility_True:
                cv2.circle(frame, right_shoulder_point, 4, (0,0,255), -1)
                cv2.circle(frame, elbow_point, 4, (0,0,255), -1)
                cv2.circle(frame, right_wrist_point, 4, (0,0,255), -1)
                cv2.circle(frame, left_shoulder_point, 4, (0,0,255), -1)
                cv2.circle(frame, left_hip_point, 4, (0,0,255), -1)
                cv2.circle(frame, right_hip_point, 4, (0,0,255), -1)
                cv2.circle(frame, right_ear_point, 4, (0,0,255), -1)
                
                #line up the circles

                cv2.line(frame, right_shoulder_point, elbow_point, (255,0,0), 2)
                cv2.line(frame, elbow_point, right_wrist_point, (255,0,0), 2)
                cv2.line(frame, right_shoulder_point, left_shoulder_point, (255,0,0), 2)
                cv2.line(frame, right_hip_point, left_hip_point, (255,0,0), 2)

                # cv2.putText(frame,f"elbow to wrist: {angle1:.1f}", (right_wrist_point), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                # cv2.putText(frame, f"elbow to wrist: {angle2:.1f}", (right_shoulder_point), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)





        cv2.imshow("pic",frame)

        if cv2.waitKey(1) == ord("q"):
            break


    #final checks and prints
    if angle_2_list.count("g") >= 2:
        print("good elbow placement on the final swing good contact point")
    else:
        print("bad contact point, have elbow facing the celing to get a higher contact point")

    if elbow_height_check.count("g") >= 4:
        print("good elbow height and position during swing")
    else:
        print("during swing elbow has to be positioned higher, facing the ceiling (not all the way).")

    if not elbow_farther_ear_horizontally_done:
        ("elbow must be farther than the ear")
    
    if shoulders_rotated_done == True:
        print("good body rotation")
    else:
        print("you need to rotate your shoulders and hips all the way during your swing")


    if not pos_3_angle_check:
        print("you need a higher contact point")


    print(elbow_height_check)
    print(angle_2_list)



    cap.release()
    cv2.destroyAllWindows()


    
else:
    print("Invalid choice! Please restart and type 'left' or 'right'.")
