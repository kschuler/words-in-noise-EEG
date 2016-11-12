#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
WORDS IN NOISE EEG EXPERIMENT
for Kelly (Turkeltaub Lab)

OSX: El Capitan (Should work on most new-ish OSX and Windows)
PsychoPy Version: 1.84.1

Written by: Kathryn Schuler (kathryn.schuler@gmail.com)
Written on: 09/29/2016
Last Updated: 11/11/2016

Expeirment version: 2.1
"""

"""
*********************************************************************************
LOAD REQUIRED PACKAGES AND SET AUDIO DRIVER PREFERENCES
*********************************************************************************
"""

# import the required packages and libraries for the experiment
from psychopy import prefs, gui, core, data, visual, info, sound, event
import time, os, numpy, yaml, glob

# set the preferred audio driver for this machine
prefs.general['audioLib'] = ['pyo']
prefs.general['audioDriver'] = ['portaudio']


"""
*********************************************************************************
SETUP EXPERIMENT PARAMTERS
*********************************************************************************
"""

# experiment parameters are loaded into a dictionary from the params.yaml file
PARAMS = yaml.safe_load(open('params.yaml', 'r'))

# get some addiitonal info about the participant via a dialogue box
# user-input parameters are set in the params.yaml file and we just
# get a timestamp for date-run
PARTICIPANT_INFO = PARAMS['experiment info']['user-input']
PARTICIPANT_INFO['date-run'] = data.getDateStr()

if not gui.DlgFromDict(PARTICIPANT_INFO, fixed = 'date', title = PARAMS['experiment info']['exp-name']).OK:
    core.quit()

"""
*********************************************************************************
 The main experiment class, which contains all the experiments objects and methods.
*********************************************************************************
"""
class WordsInNoiseEEG(object):
    def __init__(self):
        self.EXPERIMENT_DATA = data.ExperimentHandler(
            # setup the main experiment data object to keep track of all of our data
            # extra info for this could include both the EXPINFO from input and also
            # a term for {'params': PARAMS} so that it gets saved in the subject's data file
            name            = PARAMS['experiment info']['exp-name'],
            extraInfo       = PARTICIPANT_INFO,
            runtimeInfo     = info.RunTimeInfo,
            dataFileName    = PARAMS['experiment info']['data-path'] + PARTICIPANT_INFO['subject'] + '_' + PARTICIPANT_INFO['date-run']
        )
        self.EXP_WINDOW = visual.Window(
            # setup the main experiment window / screen
            screen          = PARAMS['devices']['monitor']['screen'],
            units           = PARAMS['devices']['monitor']['units'],
            color           = PARAMS['devices']['monitor']['background color'],
            fullscr         = PARAMS['devices']['monitor']['full screen']
        )
        self.INSTRUCTIONS = visual.TextStim(self.EXP_WINDOW,
            # the visual features of the main instructions for the experiment (and the rest instructions)
            text            = '',
            units           = PARAMS['stimuli']['instructions']['units'],
            pos             = PARAMS['stimuli']['instructions']['pos'],
            color           = PARAMS['stimuli']['instructions']['color'],
            height          = PARAMS['stimuli']['instructions']['height'],
            font            = PARAMS['stimuli']['instructions']['font']
        )
        self.BLOCK_TITLE = visual.TextStim(self.EXP_WINDOW,
            # the visual features of the block title
            text            = '',
            units           = PARAMS['stimuli']['block title']['units'],
            pos             = PARAMS['stimuli']['block title']['pos'],
            color           = PARAMS['stimuli']['block title']['color'],
            height          = PARAMS['stimuli']['block title']['height'],
            font            = PARAMS['stimuli']['block title']['font']
        )
        self.DIFFICULTY_TEXT = visual.TextStim(self.EXP_WINDOW,
            # the visual features of the text that appears to tell you the difficult level (H or E)
            text            = '',
            units           = PARAMS['stimuli']['difficulty text']['units'],
            pos             = PARAMS['stimuli']['difficulty text']['pos'],
            color           = PARAMS['stimuli']['difficulty text']['color'],
            height          = PARAMS['stimuli']['difficulty text']['height'],
            font            = PARAMS['stimuli']['difficulty text']['font']
        )
        self.FIXATION_CROSS = visual.TextStim(self.EXP_WINDOW,
            # the visual features of the fixation cross
            text            = '+',
            units           = PARAMS['stimuli']['fixation cross']['units'],
            pos             = PARAMS['stimuli']['fixation cross']['pos'],
            color           = PARAMS['stimuli']['fixation cross']['color'],
            height          = PARAMS['stimuli']['fixation cross']['height'],
            font            = PARAMS['stimuli']['fixation cross']['font']
        )
        self.IMAGE_MASK = visual.GratingStim(self.EXP_WINDOW,
            texRes             = PARAMS['stimuli']['image mask']['tex'],
            mask            = PARAMS['stimuli']['image mask']['mask'],
            size            = PARAMS['stimuli']['image mask']['size'],
            units           = PARAMS['stimuli']['image mask']['units'],
        )
        self.STIMULUS_SOUND = sound.Sound(value = 'Sounds/pinknoise.wav',
            sampleRate = PARAMS['stimuli']['word']['sampleRate']
        )
        self.THIS_TRIAL_SOUND = sound.Sound(value = 'Sounds/pinknoise.wav',
            sampleRate = PARAMS['stimuli']['word']['sampleRate']
        )
        self.LEFT_ANSWER = visual.TextStim(self.EXP_WINDOW,
            text            = '',
            units           = PARAMS['stimuli']['answers']['left']['units'],
            pos             = PARAMS['stimuli']['answers']['left']['pos'],
            height          = PARAMS['stimuli']['answers']['left']['height'],
            color           = PARAMS['stimuli']['answers']['left']['color'],
            font            = PARAMS['stimuli']['answers']['left']['font']
        )
        self.RIGHT_ANSWER = visual.TextStim(self.EXP_WINDOW,
            text            = '',
            units           = PARAMS['stimuli']['answers']['right']['units'],
            pos             = PARAMS['stimuli']['answers']['right']['pos'],
            height          = PARAMS['stimuli']['answers']['right']['height'],
            color           = PARAMS['stimuli']['answers']['right']['color'],
            font            = PARAMS['stimuli']['answers']['right']['font']
        )
        self.UP_ANSWER = visual.TextStim(self.EXP_WINDOW,
            text            = '',
            units           = PARAMS['stimuli']['answers']['up']['units'],
            pos             = PARAMS['stimuli']['answers']['up']['pos'],
            height          = PARAMS['stimuli']['answers']['up']['height'],
            color           = PARAMS['stimuli']['answers']['up']['color'],
            font            = PARAMS['stimuli']['answers']['up']['font']
        )
        self.DOWN_ANSWER = visual.TextStim(self.EXP_WINDOW,
            text            = '',
            units           = PARAMS['stimuli']['answers']['down']['units'],
            pos             = PARAMS['stimuli']['answers']['down']['pos'],
            height          = PARAMS['stimuli']['answers']['down']['height'],
            color           = PARAMS['stimuli']['answers']['down']['color'],
            font            = PARAMS['stimuli']['answers']['down']['font']
        )

    def run_experiment(self):

        # the main experiment loop, which runs all the phases of the experiment
        # each phase is its own function
        self.setup_experiment()
        self.display_instructions()
        self.do_task('baseline staircase')
        self.do_task('main staircase')
        self.end_experiment()


    def setup_experiment(self):

        # things we need to do before the experiment begins. Note that we do not preload
        # all of the stimuli here. It is much less memory intensive to handle them one
        # at a time in the inter-trial interval (1 second is plenty of time to do this)
        # only when they are needed. here we get the monitor refresh rate (used to calculate jitter window)
        # and also set the mouse visibility and build the staircases we are going to need
        self.EXP_WINDOW.mouseVisible = PARAMS['devices']['mouse']['visible']
        self.ACTUAL_REFRESH_RATE = self.EXP_WINDOW.getActualFrameRate(nMaxFrames = 100, nWarmUpFrames = 20, threshold = 1)
        self.STIMS = yaml.safe_load(open('conditions.yaml', 'r'))

        # generate the stiarcase for this experiment from the parameter file
        self.build_the_staircases(PARAMS['staircases'])


    def display_instructions(self):

        # for each of the instruction pages (params.yaml), set the correct text, draw them to the screen, and
        # flip the window to display them.  Wait for the 'space' key to move on.
        for instructions in PARAMS['stimuli']['instructions']['pages']:
            self.INSTRUCTIONS.setText(instructions)
            self.INSTRUCTIONS.draw()
            self.EXP_WINDOW.flip()
            event.waitKeys(PARAMS['devices']['keyboard']['keys next'])


    def do_task(self, which_staircase):

        # if this is the main staircase, pull the values from the baseline staircases
        # to use as start values in the main staircase
        if which_staircase == 'main staircase':
            self.get_baseline_thresholds()

        # create a variable to hold what block number we are on
        this_block = 0

        # for all of the blocks in the available staircases
        for block in self.randomize_blocks(which_staircase):

            this_block += 1
            self.CONDITION = block

            # enter the staircase and let the data handler know we have done so
            this_staircase = self.STAIRCASE_HANDLER[which_staircase][block]
            self.EXPERIMENT_DATA.addLoop(this_staircase)

            # show which block we are doing (Auditory, Visual, Environmental)
            self.display_block_title_screen(self.CONDITION)

            # for all of the trials that we are supposed to do per block in this stiarcase
            for trial in range(PARAMS['method']['reps'][which_staircase]['trials per block']):

                # add some data about which condition and block it is
                this_staircase.addOtherData('condition', self.CONDITION)
                this_staircase.addOtherData('block', this_block)

                # get the loudness we should set stim at and the params of this step in the staircase
                this_loudness, this_step = this_staircase.next()

                # do each portion of the trail
                self.intertrial_interval(this_loudness, this_step)
                self.prestimulus_period(this_step)
                self.stimulus_presentation_window()
                self.poststimulus_waiting_period()
                is_correct = self.answer_choice_period() # return is correct

                # tell the staircase whether we got this step right
                this_staircase.addResponse(is_correct)

                # tell the data handler that we are finshed with that trial and about to start a new trial
                self.EXPERIMENT_DATA.nextEntry()

                # if somebody presses escape on any trial, quit the experiment
                if event.getKeys(PARAMS['devices']['keyboard']['keys quit']): self.end_experiment()

            # if this is a block we are supposed to take a rest after, do so
            if this_block in PARAMS['method']['reps'][which_staircase]['rest after blocks']:
                self.do_rest_period()


    def end_experiment(self):

        # this is just a cleanup function that closes the experiemnt
        # window and quits psychopy
        self.EXP_WINDOW.close()
        core.quit()

    def randomize_blocks(self, which_staircase):

        # Take each condition (Auditory, Visual, Environmental) and randomly
        # permute them however many times are specified in number of blocks per condition.
        BLOCKS = []
        for _ in range(PARAMS['method']['reps'][which_staircase]['blocks per condition']):
            for condition in numpy.random.permutation(PARAMS['method']['conditions']): BLOCKS.append(condition)

        # returns the list of randomized blocks for the staircase
        return BLOCKS


    def display_block_title_screen(self, this_condition):

        # set the text for the particular block, draw it to the screen and flip
        # the window.  Wait for the time specified in 'block title screen'
        self.BLOCK_TITLE.setText(this_condition)
        self.BLOCK_TITLE.draw()
        self.EXP_WINDOW.flip()
        core.wait(PARAMS['method']['timing']['block title screen'])


    def build_the_staircases(self, all_staircases):

        # here we build all of the staircases we will use in the experiment.  This is handled by creating a
        # MultiStairHandler for each condition (Auditory, Visual, and Environmental).  Each multistair
        # has an easy and a hard staircase, and they are interleaved (selected at random such that not more than
        # three of the same difficulty level are selected in a row).  All staircases are QUEST adaptive staircases
        # with parameters set from the params.yaml file

        # make an empty dictionary to hold the staircases
        self.STAIRCASE_HANDLER = {}

        # for all of the staircases (in params - baseline and main)
        for staircase in all_staircases:

            # create an empty dictionary
            self.STAIRCASE_HANDLER[staircase] = {}

            # and add a multistair handler for each condition (Auditory, Visual, and Environmental)
            for condition in PARAMS['method']['conditions']:
                self.STAIRCASE_HANDLER[staircase].update({condition: data.MultiStairHandler(
                        stairType = 'simple',
                        method = 'random',
                        conditions = [PARAMS['staircases'][staircase][condition]['easy'], PARAMS['staircases'][staircase][condition]['hard']],
                        nTrials = PARAMS['method']['reps'][staircase]['trials per staircase']
                        # name = staircase+" "+condition
                        )})



    def intertrial_interval(self, trial_volume, trial_params):

        # start the precise timer
        self.start_precise_timer(PARAMS['method']['timing']['intertrial interval'])

        # draw the fixation cross in gray and flip the window
        self.FIXATION_CROSS.setColor('gray')
        self.FIXATION_CROSS.draw()
        self.EXP_WINDOW.flip()

        # preload the stimuli we need for this trial during this time.
        self.preload_stimulus(trial_volume, trial_params)

        # stop the precise timer and save whether it was accurate on this trial
        timer_accuracy = self.stop_precise_timer()
        self.EXPERIMENT_DATA.addData('intertrial_interval', timer_accuracy)



    def prestimulus_period(self, trial_params):

        # start the precise timer
        self.start_precise_timer(PARAMS['method']['timing']['prestimulus period'])

        # set which text will appear on the screen
        if trial_params['label'] == 'easy': diff_text = 'E'
        else: diff_text = 'H'

        # draw the E or the H and flip the window
        self.DIFFICULTY_TEXT.setText(diff_text)
        self.DIFFICULTY_TEXT.draw()
        self.EXP_WINDOW.flip()

        # start playing the mixed sound file
        self.STIMULUS_SOUND.play()

        # stop the precise timer and save whether it was accurate on this trial
        timer_accuracy = self.stop_precise_timer()
        self.EXPERIMENT_DATA.addData('prestimulus_period', timer_accuracy)



    def stimulus_presentation_window(self):

        # start the precise timer
        self.start_precise_timer(PARAMS['method']['timing']['stimulus presentation window'])

        # jitter the start time
        self.jitter_start_time()

        # fade in the stim depending on what we have got.
        # self.fade_in_stimulus()

        # send the trigger here probably
        self.send_ttl_trigger('stim presentation window')

        # play the movie and/or sound and/or noisemask
        self.play_stimulus()

        # stop the precise timer and save whether it was accurate on this trial
        timer_accuracy = self.stop_precise_timer()
        self.EXPERIMENT_DATA.addData('stimulus_presentation_window', timer_accuracy)


    def poststimulus_waiting_period(self):

        # start the precise timer
        self.start_precise_timer(PARAMS['method']['timing']['post stimulus waiting period'])

        # make the fixation cross red and draw it to the screen
        self.FIXATION_CROSS.setColor('red')
        self.FIXATION_CROSS.draw()
        self.EXP_WINDOW.flip()

        # stop the precise timer and save whether it was accurate on this trial
        timer_accuracy = self.stop_precise_timer()
        self.EXPERIMENT_DATA.addData('poststimulus_waiting_period', timer_accuracy)


    def answer_choice_period(self):

        # create a dictionary of answer positions (keys) assigned to
        # the text stims in those positions (values)
        ANSWER_POSITIONS = {
            'left': self.LEFT_ANSWER,
            'right': self.RIGHT_ANSWER,
            'up': self.UP_ANSWER,
            'down':self.DOWN_ANSWER
        }

        # randomly shuffle the answer choices and assign them to ANSWER_POSITIONS
        # draw each one and then flip the window after all 4 are drawn
        numpy.random.shuffle(self.ANSWER_CHOICES)
        for pos in ANSWER_POSITIONS.itervalues():
            pos.setText(self.ANSWER_CHOICES.pop())
            pos.draw()
        self.EXP_WINDOW.flip()

        # wait for the participant to press a key (for time specified in timeout)
        # return the key they pressed and their reaction time (RT)
        # return whether their choice was correct (for data storing purposes)
        try:
            selection, RT = event.waitKeys(maxWait=PARAMS['method']['timing']['answer choice timeout'], keyList=ANSWER_POSITIONS.keys(), timeStamped = True)[0]
            this_choice = ANSWER_POSITIONS[selection].text
            if this_choice == self.TRIAL_SOUND: is_correct = True
            else: is_correct = False
        except TypeError:
            selection, RT, this_choice = ['NA'] * 3
            is_correct = False

        # add the data we have collected to the data manager
        self.EXPERIMENT_DATA.addData('correct_answer', self.TRIAL_SOUND)
        self.EXPERIMENT_DATA.addData('answer_choice_position', selection)
        self.EXPERIMENT_DATA.addData('answer_choice', this_choice)
        self.EXPERIMENT_DATA.addData('is_correct', is_correct)
        self.EXPERIMENT_DATA.addData('RT', RT)

        return is_correct


    def play_stimulus(self):
        # if we are at the movie, play it.  otherwise draw noise
        if self.CONDITION == "Visual":
            self.MOVIE.seek(0.0)
            self.MOVIE.setVolume(0.0)

            # play the word and the movie at the same time
            # self.WORD.play()
            self.MOVIE.play()

            # while the movie is still playing, draw it (and the mask if needed)
            while self.MOVIE.status != visual.FINISHED:
                self.MOVIE.draw()
                # if it is not a visual trial, show the noise mask
                self.EXP_WINDOW.flip()

        else:
            # play the word and the image mask at the same time
            # self.WORD.play()
            self.IMAGE_MASK.draw()
            self.EXP_WINDOW.flip()


    def preload_stimulus(self, trial_volume, trial_params):

        # this function preloads the stimuli necessary for the trial.  Note that it always loads the corresponding video
        # and an image mask to make it equal for both trials.  But it only uses one later on.

        # randomly choose a sound the play from the remaining trials in this staircase
        remaining_trials = self.STIMS[trial_params['staircase']][trial_params['condition']][trial_params['label']]
        self.ANSWER_CHOICES = remaining_trials.pop(numpy.random.choice(remaining_trials.keys()))
        self.TRIAL_SOUND = self.ANSWER_CHOICES[0]

        print "loading ", self.TRIAL_SOUND
        print "remaining trials ", remaining_trials

        # load the movie and make sure the volume is 0.
        self.MOVIE = visual.MovieStim2(self.EXP_WINDOW,
            filename ='Movies/'+self.TRIAL_SOUND+'.mov',
            volume = 0.0,
            pos = PARAMS['stimuli']['movie']['pos'],
            size = PARAMS['stimuli']['movie']['size']
        )
        self.MOVIE.setVolume(0.0)

        # load the image mask
        self.IMAGE_MASK.setTex(numpy.random.random((32,32)))

        # pull the actual sound file to retrieve duration
        which_sound_file = 'Sounds/'+trial_params['condition']+'/'+trial_params['label']+'/'+self.TRIAL_SOUND+'.wav'

        # get the duration of the sound and calculate jitter
        self.THIS_TRIAL_SOUND.setSound(which_sound_file)
        self.calculate_jitter(self.THIS_TRIAL_SOUND.getDuration())

        # mix the sounds
        self.mix_sound_sox(noise_file = 'Sounds/noise.wav',
            noise_volume = 1.0,
            stimulus_file = 'Sounds/'+trial_params['condition']+'/'+trial_params['label']+'/'+self.TRIAL_SOUND+'.wav',
            stimulus_volume = trial_volume)

        # preload the output sound and set it to full volume
        self.STIMULUS_SOUND.setSound('Sounds/mixed_sound_output.wav')
        self.STIMULUS_SOUND.setVolume(1.0)


        print trial_volume, trial_params


    def mix_sound_sox(self, noise_file, noise_volume, stimulus_file, stimulus_volume):
        stimulus_padding = PARAMS['method']['timing']['prestimulus period'] + self.RANDOM_ONSET_TIME
        print stimulus_padding
        os.system('sox -V --combine mix -v '+str(noise_volume)+' '+noise_file+' -v '+str(stimulus_volume)+' "|sox '+stimulus_file+' -p pad '+str(stimulus_padding)+' " Sounds/mixed_sound_output.wav')


    def start_precise_timer(self, duration):

        self.timer = core.StaticPeriod(screenHz = PARAMS['devices']['monitor']['screenHz'])
        self.timer.start(duration)


    def stop_precise_timer(self):

        timer_accuracy = self.timer.complete()
        self.EXP_WINDOW.flip()

        # returns the accuracy of the timer
        return timer_accuracy

    #
    def calculate_jitter(self, stim_duration):

        # get the variables we need to calculate the jitter
        jitter_window = PARAMS['method']['timing']['stimulus presentation window']
        offset_buffer = PARAMS['method']['timing']['stimulus offset buffer']
        seconds_per_frame = 1/PARAMS['devices']['monitor']['screenHz']


        print self.TRIAL_SOUND, stim_duration
        print jitter_window, offset_buffer, seconds_per_frame

        # take the stimuli duration and figure out possible start times that would end
        # within the stim presntation window.  use a bugger to make sure we don't cut it too close
        # to the end of the window
        possible_jitter = (jitter_window - offset_buffer) - stim_duration
        possible_onset_times = numpy.arange(seconds_per_frame, possible_jitter, seconds_per_frame)

        print possible_jitter, possible_onset_times

        # choose a random onset time from these options and return it
        # try:
        self.RANDOM_ONSET_TIME = numpy.random.choice(possible_onset_times)
        # except ValueError:
        #     print "Sorry, the current stimulus is too long to play in the stimulus presentation window"
        # while we are waiting, add the actual onset and offset times to the data filename
        self.EXPERIMENT_DATA.addData('actual_onset_time', self.RANDOM_ONSET_TIME)
        self.EXPERIMENT_DATA.addData('actual_offset_time', self.RANDOM_ONSET_TIME + self.THIS_TRIAL_SOUND.getDuration())

        print self.RANDOM_ONSET_TIME


    def jitter_start_time(self):

        # wait for start time
        core.wait(self.RANDOM_ONSET_TIME)


    def fade_in_stimulus(self):

        # start the opacity at 0 and get the number of frames to fade the movie over
        opacity = 0.0
        nFrames = 30

        print "number of frames ", nFrames

        # start playing the movie but pause on the first frame
        self.MOVIE.play()
        self.MOVIE.pause()

        # fade in the movie over the specified frames
        for frame in range(nFrames):
            opacity += (1.0/nFrames)
            self.MOVIE.setOpacity(opacity)
            self.MOVIE.draw()
            self.EXP_WINDOW.flip()

    def do_rest_period(self):

        # set the instructions for the rest period, draw them, and
        # wait for however long is specified in REST_BLOCK_DURATION
        self.INSTRUCTIONS.setText(PARAMS['stimuli']['instructions']['rest instructions'])
        self.INSTRUCTIONS.draw()
        self.EXP_WINDOW.flip()
        core.wait(PARAMS['method']['timing']['rest block duration'])

    def send_ttl_trigger(self, name = None):
        print name
        # this is not doing anything yet; here is where you would add the code to
        # send the ttl trigger.  It is likely very short, just a few lines
        # and you'll need to use psychopy's parallel library to send it
        pass

    def get_baseline_thresholds(self):

        thresholds = {}

        for condition in PARAMS['method']['conditions']:
            easy, hard = self.STAIRCASE_HANDLER['baseline staircase'][condition].staircases
            thresholds[condition] = {'easy': easy.intensities[-1], 'hard': hard.intensities[-1]}

        for condition in PARAMS['method']['conditions']:
            easy, hard = self.STAIRCASE_HANDLER['main staircase'][condition].conditions
            print easy, hard
            easy['startVal'] = thresholds[condition]['easy']
            hard['startVal'] = thresholds[condition]['hard']

            print easy, hard
            print self.STAIRCASE_HANDLER['main staircase'][condition].conditions



exp = WordsInNoiseEEG()
exp.run_experiment()
