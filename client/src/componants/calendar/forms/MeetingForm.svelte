<script lang="ts">
    import Input from '../../ui/Input.svelte';
    import ModalOpenButton from '../../ui/modals/ModalOpenButton.svelte';
    import Submit from '../../ui/Button.svelte';
    //import ModalCloseButton from '../modal/ModalCloseButton.svelte';
    import Modal from '../../ui/modals/SimpleModal.svelte';
    import PeopleSelect from '../../ui/select/UsersMultiSelect.svelte';
    import CalendarDataService from '../../../apis/home/home';
    import { UserStore } from '../../../utils/stores';
    import type { calendarItemsType, SelectOptionType } from '../../../utils/types';
    import { createEventDispatcher } from 'svelte';
    import { isValidDate } from '../../../utils/validations';
  
    export let startDate: string;
    export let isError: boolean = false;
    export let datePickerDisabled: boolean = false;
    export let isLoading: boolean = false;
    
    // if true the disable submit button
    const modalID = 129981;

    let responseMeeting: calendarItemsType;
    const dispatch = createEventDispatcher();

    let meetingLocationValue: string;
    let meetingLocationIsError: boolean | null = null;
    let meetingLinkValue: string;
    let meetingLinkIsError: boolean | null = null;
    let meetingTimeValue: string;
    let meetingTimeIsError: boolean | null = null;
  
    let meetingPeopleIsError: boolean | null = false;
  
    let peopleSelected: SelectOptionType[] = [];
    $: fillDisabled =
      meetingLocationIsError === null ||
      meetingLocationIsError === true ||
      meetingPeopleIsError === null ||
      meetingPeopleIsError === true ||
      datePickerDisabled ||
      peopleSelected.length === 0;

    let submitDisabled = true;

    $: submitDisabled =
      fillDisabled ||
      meetingLinkIsError === null ||
      meetingLinkIsError === true ||
      meetingTimeIsError === true ||
      meetingTimeIsError === null ||
      peopleSelected.length === 0;
    const modalData = {
      'data-bs-dismiss': 'modal',
      'data-bs-target': `#modal${modalID}`,
      'aria-label': 'Close',
    };
</script>

<form>
    <PeopleSelect
        isTop={true}
        placeholder={"Select Users.."}
        bind:isError={meetingPeopleIsError}
        bind:selected={peopleSelected}
    />
    <Input
        type="text"
        label={'Location'}
        bind:value={meetingLocationValue}
        handleInput={() => {
            return false;
        }}
        size={20}
        errorMessage="location is invalid"
        hint={'please write a valid location'}
        placeholder={'Meeting Location'}
        bind:isError={meetingLocationIsError}
    />
    <div class="width-100 mt-4">
        <ModalOpenButton width={100} label="Fill" bind:disabled={fillDisabled} {modalID} />
    </div>
</form>
  
<Modal
    id={modalID + ''}
    isDelete={false}
    isDone={false}
    isFooter={true}
    doneText={'Done'}
    deleteText={'Delete'}
    isClose={true}
>
    <header slot="header">
        <h6>???? Meeting Form</h6>
    </header>
  
    <form slot="form">
      {#if isError}
        <div class="alert alert-danger" role="alert">
          <strong>Oh snap!</strong> Change a few things up and try submitting again.
        </div>
      {:else if isLoading}
        <div class="alert alert-info" role="alert">
          <strong>Loading...</strong> Please wait.
        </div>
      {:else}
        <Input
          type="text"
          label={'Meeting Link'}
          bind:value={meetingLinkValue}
          handleInput={() => {
            return false;
          }}
          size={20}
          errorMessage="Meeting Link is invalid"
          hint={'please write a valid link'}
          placeholder={'Meeting Link'}
          bind:isError={meetingLinkIsError}
        />
        <Input
          type="time"
          label={'Meeting Time'}
          bind:value={meetingTimeValue}
          handleInput={() => {
            return false;
          }}
          size={20}
          errorMessage="Meeting Time is invalid"
          hint={'please write a valid time'}
          placeholder={'Meeting Time'}
          bind:isError={meetingTimeIsError}
        />
      {/if}
    </form>
  
    <div slot="submit">
      <Submit
        successMessage={'Meeting is Scheduled'}
        errorMessage={'Meeting Submission Failed'}
        {modalData}
        label="Post Meeting!"
        onClick={async () => {
          isLoading = true;
          try {
            const invited_people = peopleSelected.map((person) =>
              Number(person.value)
            );
            let time = meetingTimeValue;
            if (time.split(':')[0] == "00"){
              time.split(':')[0] = "12"
            };
            const axios = await CalendarDataService.postMeeting({
              hostedUserID: $UserStore.id,
              date: startDate,
              invitedUsers: invited_people,
              location: meetingLocationValue,
              meetingLink: meetingLinkValue,
              time: time,
            });
            isLoading = false;
            meetingLocationValue = '';
            meetingTimeValue = '';
            meetingLinkValue = '';
            peopleSelected = [];
            responseMeeting = axios.data.results
            dispatch('message', {
                postedMeeting: responseMeeting
            });
          } catch (error) {
            isError = true;
          } finally {
            isLoading = false;
            meetingLocationValue = '';
            meetingTimeValue = '';
            meetingLinkValue = '';
            peopleSelected = [];
          }
          return isError;
        }}
        bind:disabled={submitDisabled}
      />
    </div>
</Modal>
  