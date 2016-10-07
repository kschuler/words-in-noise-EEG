#!/usr/bin/env python
"""
SAMPLE TASK FOR KELLY

OSX: El Capitan (Should work on most new-ish OSX)
PsychoPy Version: 1.84.1

Written by: Kathryn Schuler (kathryn.schuler@gmail.com)
Written on: 09/29/2016
Last Updated: 10/03/2016
"""
"""
*********************************************************************************
SETUP EXPERIMENT PARAMTERS
*********************************************************************************
"""
# set the parameters of the dialog box (what participant info do you want it to ask for?)
# it is a dictionary (EXP_INFO) that can have any number of key-value pairs
# you can add as many as you want to
EXP_TITLE = "Kelly's sample experiment"          # name the experiment here
EXP_INFO = {                                     # used to generate dialogue box to request info
    'subject':'',                                # subject ID (requests typing)
    'gender': ['male', 'female'],                # gender (input box with 2 values)
    'hand': ['right', 'left'],
    'id': ''

}

# task relevant parameters (how many times to do things; randomize or not, etc.)
CONDITIONS = ['Auditory', 'Visual']             # the conditions of the experiment
TRIALS_PER_BLOCK = 2                            # number of trials per block
BLOCKS_PER_CONDITION = 8                        # total number of blocks in the experiment
REST_AFTER_BLOCKS = [1,2]                       # take a rest after these blocks (a list of block numbers)
CONDITION_METHOD = 'random'                     # 'random' or 'sequential' read conditions file
CONDITION_NREPS  = 1                            # number of times to repeat a conditions file

# timing parameters / how long to do things for. IMPORTANT: if you alter these to be values that are not
# complete seconds, you will need to add something that will convert the values using the frame rate
# e.g. you can't start or stop something at 40 ms if you have a frame-rate of 60Hz.  You're only options are
# 33.3333 ms or 50 ms, so your timing will be off by a little this makes sure times are aligned to
# frame-rate and outputs these into the datafile
TITLE_SCREEN_DURATION = 1.0
REST_BLOCK_DURATION = 2.0
INTERTRIAL_INTERVAL_DURATION = 1.0
PRESTIMULUS_PERIOD_DURATION = 1.0
STIMULUS_PRESENTATION_WINDOW = 2.050
STIMULUS_OFFSET_BUFFER = 0.050
POSTSTIMULUS_WAITING_PERIOD_DURATION = 1.0
ANSWER_CHOICE_TIMEOUT = 3.0
REST_BLOCK_DURATION = 20.0


# setup all of the visual parameters of the experiment; how you want the text to look,
# where to display it, what color, etc
# visual window parameters (display)
DISPLAY_MONITOR = 0                             # which monitor to display on (usually 0, but could be 1 or 2)
DISPLAY_COLOR = 'black'                         # what color is the background ('white', 'black', 'gray' or a HEX)
DISPLAY_FULLSCREEN = False                     # best to test at False, but run subjects in True
DISPLAY_MOUSE = False                            # whether or not to display the mouse (True or False)

# instructions text (sets initial instructions and rest block text)
INSTRUCTIONS_POS = [0,0]                        # [x,y] position of the text ([0,0] is center)
INSTRUCTIONS_COLOR = 'gray'                     # color of the text (psychopy knows some simple words like 'gray', but can also be HEX or RGB
INSTRUCTIONS_HEIGHT = 20                        # font size

# block text (sets the text that tells participants what condition is happening)
BLOCK_POS = [0,0]                               # [x,y] position of the text ([0,0] is center)
BLOCK_COLOR = 'gray'                            # color of the text (psychopy knows some simple words like 'gray', but can also be HEX or RGB
BLOCK_HEIGHT = 40                               # font size

# level text (sets the text that tells participants the difficulty level)
LEVEL_POS = [0,0]                               # [x,y] position of the text ([0,0] is center)
LEVEL_COLOR = 'gray'                            # color of the text (psychopy knows some simple words like 'gray', but can also be HEX or RGB
LEVEL_HEIGHT = 40                               # font size

# fixation cross (sets the position, color, and size of the fixation cross)
FIXATION_POS = [0,0]                            # [x,y] position of the text ([0,0] is center)
FIXATION_COLOR = 'gray'                         # color of the cross (psychopy knows some simple words like 'gray', but can also be HEX or RGB
FIXATION_HEIGHT = 40                            # font height of cross

# parameters of the video files (setting the size correctly is very important for timing precision).
MOVIE_SIZE = [720, 400]
MOVIE_VOLUME = 0.0
MOVIE_POS = [0,0]


# instruction parameters; what the instruction text says. use triple quotes
# to span multiple lies (""" """).
INSTRUCTIONS_PAGE1 = "page 1, space to continue."
INSTRUCTIONS_PAGE2 = "page 2, space to continue."
INSTRUCTIONS_PAGE3 = "page 3, space to continue. "
INSTRUCTIONS_PAGE4 = "page 4, space to continue (start)."
REST_TEXT = "You will now be given a 2 minute break.  The experiment will resume automatically."


"""
*********************************************************************************
PRESENT DIALOG BOX TO GET PARTICIPANT INFO (MUST HAPPEN FIRST)
*********************************************************************************
"""
# you have to do the gui before you import the visual package or the screen
# gets messed up on OSX.  So we import gui and core, packages we need now
from psychopy import gui, core, data

# Request user input with dialog box and quit if they do not
# fill it out properly or user hits cancel
EXP_INFO['date'] = data.getDateStr()

if not gui.DlgFromDict(EXP_INFO, fixed = 'date', title = EXP_TITLE).OK:
    core.quit()
else: print "running participant: "+str(EXP_INFO['subject'])+" in "+ str(EXP_TITLE)


"""
*********************************************************************************
LOAD REQUIRED PACKAGES AND SET AUDIO DRIVER PREFERENCES
*********************************************************************************
"""
# import the libraries we need to use
from psychopy import visual, info, sound, event
import time, os, numpy

# make sure we set the correct audio driver and libraries for precision
# (portaudio is preferred on mac and pyo is the most precise audio handler)
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
prefs.general['audioDriver']= ['portaudio']


"""
*********************************************************************************
 The main experiment class, which contains all the experiments objects and methods.
*********************************************************************************
"""
class KellyExperiment(object):
    def __init__(self):

        # setup the main experiment data object to keep track of all of our data
        self.experiment_data = data.ExperimentHandler(name = EXP_TITLE, extraInfo = EXP_INFO,
            runtimeInfo = info.RunTimeInfo, dataFileName = 'data/'+EXP_INFO['subject']+"_"+EXP_INFO['date'])

        # setup the main experiment window / screen
        self.exp_window = visual.Window(screen = DISPLAY_MONITOR, units = 'pix', color = DISPLAY_COLOR,
            fullscr = DISPLAY_FULLSCREEN)

        # text instructions shown on screen
        self.instructions = visual.TextStim(self.exp_window, units = 'pix', pos = INSTRUCTIONS_POS,
            text = '', color = INSTRUCTIONS_COLOR, height = INSTRUCTIONS_HEIGHT)
        self.which_phase = visual.TextStim(self.exp_window, units = 'pix', pos = BLOCK_POS,
            text = '', color = BLOCK_COLOR, height = BLOCK_HEIGHT)
        self.level = visual.TextStim(self.exp_window, units = 'pix', pos = LEVEL_POS,
            text = 'H', color = LEVEL_COLOR, height = LEVEL_HEIGHT)

        # fixation cross
        self.fixation_cross = visual.TextStim(self.exp_window, text="+", height = FIXATION_HEIGHT,color=FIXATION_COLOR, pos = FIXATION_POS)

        # stimuli
        self.image_mask = visual.GratingStim(self.exp_window, tex='stims/kelly_face_static.png', mask=None, size=256)
        self.pink_noise = sound.Sound(value = 'stims/pinknoise_3secs.wav', sampleRate = 48000)
        self.sound_audio_only = sound.Sound(value = 'stims/pinknoise_3secs.wav', sampleRate = 48000)

        # answer choices for test
        self.left_answer = visual.TextStim(self.exp_window, units = 'pix', pos = (-100, 0),
            text = 'left', color = 'gray')
        self.right_answer = visual.TextStim(self.exp_window, units = 'pix', pos = (100, 0),
            text = 'right', color = 'gray')
        self.up_answer = visual.TextStim(self.exp_window, units = 'pix', pos = (0, 100),
            text = 'up', color = 'gray')
        self.down_answer = visual.TextStim(self.exp_window, units = 'pix', pos = (0, -100),
            text = 'down', color = 'gray')


    def run_experiment(self):

        # the main experiment loop, which runs all the phases of the experiment
        # each phase is its own function
        self.setup_experiment()
        self.show_instructions()
        self.staircase_procedure()
        self.main_task()
        self.end_experiment()


    def setup_experiment(self):

        # things we need to do before the experiment begins. Note that we do not preload
        # all of the stimuli here. It is much less memory intensive to handle them one
        # at a time in the inter-trial interval (1 second is plenty of time to do this)
        # only when they are needed.  here we randomize the order of the conditions for the participant
        # and get the monitor refresh rate (used to calculate jitter window), also mouse visibility
        self.exp_window.mouseVisible = DISPLAY_MOUSE
        numpy.random.shuffle(CONDITIONS)
        self.actual_refresh_rate = round(self.exp_window.getActualFrameRate(nMaxFrames = 300, nWarmUpFrames = 20, threshold = 1))


    def show_instructions(self):

        # a list of all of the instructions you want to show before the experiment
        instructions_list = [INSTRUCTIONS_PAGE1, INSTRUCTIONS_PAGE2, INSTRUCTIONS_PAGE3, INSTRUCTIONS_PAGE4]

        # for each of theses instructions, set the correct text, draw them to the screen, and
        # flip the window to display them.  Wait for the 'space' key to move on.
        for instructions in instructions_list:
            self.instructions.setText(instructions)
            self.instructions.draw()
            self.exp_window.flip()
            event.waitKeys(keyList='space')


    def staircase_procedure(self):

        # staircase procedure not yet written but needs to output the two difficulty thresholds
        # self.hard_snr and self.easy_snr for use in the main task.  I've just set some default
        # values to use for now (these will be what the volume of the sound stimuli gets set at)
        self.hard_snr = 0.70
        self.easy_snr = 0.95


    def main_task(self):

        self.randomize_conditions()

        # # the main experiment loop
        # # for every condition in the CONDITIONS list (ranomized in setup_experiment)
        # for self.condition in CONDITIONS:
        #
        #     # load the condition file for that condition and tell the data object
        #     # there is a new experiment loop
        #     self.load_trials("conditions/"+self.condition+".xlsx")
        #     self.experiment_data.addLoop(self.condition_trials)
        #
        # for every block in all of the BLOCKS_PER_CONDITION, set the title screen
        # and then randomize the difficulty level for every trial
        for block in range(BLOCKS_PER_CONDITION):

            self.condition = next(self.EXP_CONDITIONS)
            self.block_title_screen(self.condition)
            self.randomize_difficulty_levels()

            # then for every trial per block, you do the complete trial structure
            # read the trial from the conditions file and set in this_trial,
            # intertrial_interval, then prestimulus_period, then stimulus_presentation_window,
            # then poststimulus_waiting_period, then answer_choice_period.  Each is its own function
            for trial in range(TRIALS_PER_BLOCK):

                # add some data about which condition and block it is
                self.condition_trials.addData('condition', self.condition)
                self.condition_trials.addData('block', block)

                # go to the next trial in the condition list
                this_trial = self.condition_trials.next()

                # do each part of the experiment

                self.intertrial_interval(self.condition, this_trial.stimulus, self.trial_difficulty_list[trial])
                self.prestimulus_period(self.trial_difficulty_list[trial])
                self.stimulus_presentation_window()
                self.poststimulus_waiting_period()
                self.answer_choice_period(this_trial)

                # tell the data handler that we are finshed with that trial and about to start a new trial
                self.experiment_data.nextEntry()

            # if we are on a block number that is designated in REST_AFTER_BLOCKS
            # take a break, otherwise keep going
            if block in REST_AFTER_BLOCKS: self.do_rest_period()
            else: pass



    def end_experiment(self):

        # to end the experiment, close the window and quit everything
        self.exp_window.close()
        core.quit()

    def load_trials(self, thisFile, this_method = CONDITION_METHOD, num_reps=CONDITION_NREPS):

        # load the condition files specified in thisFile accoring to the method and number of
        # reps specified in the experiment parameters
        self.conditions_file = data.importConditions(thisFile)
        self.condition_trials = data.TrialHandler(self.conditions_file, method = this_method, nReps = num_reps, extraInfo = EXP_INFO)

    def randomize_conditions(self):

        ALLCONDS = []
        for this_subblock in range(BLOCKS_PER_CONDITION):
            numpy.random.shuffle(CONDITIONS)
            for condition in CONDITIONS:
                ALLCONDS.append(condition)

        self.EXP_CONDITIONS = iter(ALLCONDS)
        print self.EXP_CONDITIONS

    def block_title_screen(self, which_condition, duration = TITLE_SCREEN_DURATION):

        # set the text for the particular block, draw it to the screen and flip
        # the window.  Wait for the time set in TITLE_SCREEN_DURATION
        self.which_phase.setText(which_condition)
        self.which_phase.draw()
        self.exp_window.flip()
        core.wait(duration)

    def randomize_difficulty_levels(self, num_each_difficulty = TRIALS_PER_BLOCK/2):

        # make a list of however many of each difficulty levels we need
        # and randomize the list for use by the main experiment
        self.trial_difficulty_list = ['H', 'E'] * num_each_difficulty
        numpy.random.shuffle(self.trial_difficulty_list)

    def intertrial_interval(self, which_block, stim_to_load, stim_volume,
        duration = INTERTRIAL_INTERVAL_DURATION):

        # draw the fixation cross in gray and flip the window
        self.fixation_cross.setColor('gray')
        self.fixation_cross.draw()
        self.exp_window.flip()

        # start a static period for the exact time of the intertrial interval duration
        # and load the stimuli during this time
        thisISI = core.StaticPeriod(screenHz = self.actual_refresh_rate, name = "intertrial_interval_actual_time")
        thisISI.start(duration)
        self.preload_stimulus(which_block, stim_to_load, stim_volume)

        # end the intertrial interval and add whether or not it was precise to the data file
        ISI_accurate = thisISI.complete()
        self.experiment_data.addData('intertrial_interval_success', ISI_accurate)


    def prestimulus_period(self, easy_or_hard, duration = PRESTIMULUS_PERIOD_DURATION):

        # draw the E or H and flip the window
        # window flip will be exactly INTERTRIAL_INTERVAL_DURATION from last flip
        self.level.setText(easy_or_hard)
        self.level.draw()
        self.exp_window.flip()

        # start a new static period exactly the PRESTIMULUS_PERIOD_DURATION
        # and play the pink noise during this time
        thisISI = core.StaticPeriod(screenHz = self.actual_refresh_rate, name = "prestimulus_period_actual_time")
        thisISI.start(duration)
        self.pink_noise.play()

        # end the prestimulus period and add whether or not it was precise to the data file
        ISI_accurate = thisISI.complete()
        self.experiment_data.addData('prestimulus_period_success', ISI_accurate)

    def stimulus_presentation_window(self, duration = STIMULUS_PRESENTATION_WINDOW):

        # start a new static period exactly the STIMULUS_PRESENTATION_PERIOD
        # you will play the stimuli during this period and also send
        # the tensor pulse (to align to the stimulus onset)
        thisISI = core.StaticPeriod(screenHz = self.actual_refresh_rate, name = "stimulus_presentation_window_actual_time")
        thisISI.start(duration)

        # jitter start time
        self.jitter_start_time()

        # play the extracted sound for BOTH conditions (never play video sound)
        # more control over the precision and can set the audio channel by hand
        self.sound_audio_only.play()


        # Send the tensor pulse as soon as the sound starts playing (or right before
        # as soon as the jitter window begins
        self.send_tensor_pulse()


        # show the visual stimuli.  If the conditon is "visual", play the video (only flip on
        # frames where you actually need to - e.g. Video is only 30Hz but screen is 60Hz)
        # Otherwise, show the image_mask (just a box of pixels with a random grayscale color)
        if self.condition == 'Visual':
            while self.movie_visual_only.status != visual.FINISHED:
                self.movie_visual_only.draw()
                self.exp_window.flip()
            self.exp_window.flip()
        else:
            self.image_mask.draw()
            self.exp_window.flip()

        # end the stimulus presentation window and add whether or not it was precise to the data file
        ISI_accurate = thisISI.complete()
        self.experiment_data.addData('stimulus_presentation_window_success', ISI_accurate)

    def poststimulus_waiting_period(self, duration = 1):

        # make the fixation cross red and draw it to the screen
        self.fixation_cross.setColor('red')
        self.fixation_cross.draw()
        self.exp_window.flip()

        # start a static period for the poststimulus waiting period
        thisISI = core.StaticPeriod(screenHz = self.actual_refresh_rate, name = "poststimulus_waiting_period_actual_time")
        thisISI.start(duration)

        # end the post stimulus waiting period and add whether or not it was precise to the data file
        ISI_accurate = thisISI.complete()
        self.experiment_data.addData('poststimulus_waiting_period_success', ISI_accurate)


    def answer_choice_period(self, which_trial, timeout = ANSWER_CHOICE_TIMEOUT):

        # create a dictionary of answer positions (keys) assigned to
        # the text stims in those positions (values)
        ANSWER_POSITIONS = {
            'left': self.left_answer,
            'right': self.right_answer,
            'up': self.up_answer,
            'down': self.down_answer
        }

        # randomly shuffle the answer choices and assign them to ANSWER_POSITIONS
        # draw each one and then flip the window after all 4 get drawn
        ANSWER_CHOICES = [which_trial.stimulus, which_trial.d1, which_trial.d2, which_trial.d3]
        numpy.random.shuffle(ANSWER_CHOICES)
        for text_stim in ANSWER_POSITIONS.itervalues():
            text_stim.setText(ANSWER_CHOICES.pop())
            text_stim.draw()
        self.exp_window.flip()

        # wait for the participant to press a key (for time specified in timeout)
        # return the key they pressed and their reaction time (RT)
        # return whether their choice was correct (for data storing purposes)
        try:
            selection, RT = event.waitKeys(maxWait=timeout, keyList=ANSWER_POSITIONS.keys(), timeStamped = True)[0]
            this_choice = ANSWER_POSITIONS[selection].text
            if this_choice == which_trial.stimulus: is_correct = True
            else: is_correct = False
        except TypeError:
            selection, RT, this_choice, is_correct = ['NA'] * 4

        # add the data we have collected to the data manager
        self.experiment_data.addData('answer_choice_position', selection)
        self.condition_trials.addData('answer_choice', this_choice)
        self.condition_trials.addData('is_correct', is_correct)
        self.condition_trials.addData('RT', RT)


    def do_rest_period(self, duration =  REST_BLOCK_DURATION):

        # set the instructions for the rest period, draw them, and
        # wait for however long is specified in REST_BLOCK_DURATION
        self.instructions.setText(REST_TEXT)
        self.instructions.draw()
        self.exp_window.flip()
        core.wait(duration)

    def preload_stimulus(self, which_block, stim_to_load, difficulty_level):

        # load the upcoming stimuli during the waiting period and calculate the jitter
        # calculatate difficulty level from staircase output variable (self.hard_snr
        # and self.easy_snr)
        if difficulty_level == 'H': stim_volume = self.hard_snr
        else: stim_volume = self.easy_snr

        # if we are doing the visual condition, setup the movie, otherwise
        # create set a random grayscale noise texture for an image stimulus
        if self.condition == 'Visual':
            self.movie_visual_only = visual.MovieStim2(self.exp_window, 'stims/movies/'+stim_to_load+'.mov',
            volume = MOVIE_VOLUME, pos=MOVIE_POS,flipVert=False, name = stim_to_load, flipHoriz=False, loop=False,
            size = MOVIE_SIZE)
        else :
            self.image_mask.setTex(numpy.random.random((16,16)))

        # pre-load sound and video files and set stim volume. Note that a new MovieStim
        # object must be instantiated for each new file and the volume must be set here as well.
        self.sound_audio_only.setSound('stims/sounds/'+stim_to_load+'.wav')
        self.sound_audio_only.setVolume(stim_volume)
        self.pink_noise.setSound('stims/pinknoise_3secs.wav')
        self.pink_noise.setVolume(1.0)

        # cacluate duration of sound and amount of possible start time jitter
        # (see calculate_jitter function for more details)
        self.stim_duration = self.sound_audio_only.getDuration()
        self.calculate_jitter(self.stim_duration)


    def calculate_jitter(self, stim_duration, jitter_window = STIMULUS_PRESENTATION_WINDOW, offset_buffer = STIMULUS_OFFSET_BUFFER):

        # take the stimuli duration and figure out the possible times it could start in 2 minutes
        possible_jitter = (jitter_window - offset_buffer) - stim_duration
        seconds_per_frame = 1/self.actual_refresh_rate
        possible_onset_times = numpy.arange(seconds_per_frame, possible_jitter, seconds_per_frame)
        self.random_onset_time = numpy.random.choice(possible_onset_times)

        print possible_jitter
        print possible_onset_times
        print self.random_onset_time

    def jitter_start_time(self):

         # start a static period that is the length of the random onset time
        start_time_jitter = core.StaticPeriod(screenHz = self.actual_refresh_rate, name = "stimulus_presentation_window_actual_time")
        start_time_jitter.start(self.random_onset_time)

        # while we are waiting, add the actual onset and offset times to the datafile
        self.condition_trials.addData('actual_onset_time', self.random_onset_time)
        self.condition_trials.addData('actual_offset_time', self.random_onset_time + self.sound_audio_only.getDuration())

        # end the static period and tell the data manager whether or not it was precise
        JITTER_SUCCESS = start_time_jitter.complete()
        self.condition_trials.addData('actual_onset_time_accurate', JITTER_SUCCESS)


    def send_tensor_pulse(self):

        # this is not doing anything yet; here is where you would add the code to
        # send the tensor pulse.  It is likely very short, just a few lines
        # and you'll need to use psychopy's I/O library to send it
        pass


# Here is where the actuall experiment starts; we setup an experiment object and
# then we do run experiment, which intiates the experiment
exp = KellyExperiment()
exp.run_experiment()
