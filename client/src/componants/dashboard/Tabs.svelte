<script lang="ts">
  import Evaluation from '../evaluation/Evaluation.svelte';
  import UserEvaluation from '../evaluation/UserEvaluation.svelte';
  import Office from '../office/Office.svelte';
  import Register from '../register/Register.svelte';
  import UserDocuments from "../userdocuments/UserDocuments.svelte"
  import VacationBalance from "../vacations/VacationBalance.svelte"
  import UserVacationBalance from "../vacations/UserVacationBalance.svelte"
  import GreatAndHint from "./GreatAndHint.svelte"
  let date: Date = new Date();
</script>

<div class="row w-100 p-4">
  <div class="col-3">
    <div
      class="nav flex-column nav-tabs text-center no-bottom-border"
      id="v-tabs-tab"
      role="tablist"
      aria-orientation="vertical"
    >
      <a
        class="nav-link navtab active mb-2 "
        id="v-tabs-vacation-balance-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-vacation-balance"
        role="tab"
        aria-controls="v-tabs-vacation-balance"
        aria-selected="false"
        >Update/Post vacations balance</a
      >
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-user-vacation-balance-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-user-vacation-balance"
        role="tab"
        aria-controls="v-tabs-user-vacation-balance"
        aria-selected="false"
        >Update User Vacation Balance</a
      >
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-home-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-home"
        role="tab"
        aria-controls="v-tabs-home"
        aria-selected="true"
        >Evaluation Form</a
      >
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-user-eval-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-user-eval"
        role="tab"
        aria-controls="v-tabs-user-eval"
        aria-selected="false"
        >User Evaluation Form</a
      >
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-user-docs-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-user-docs"
        role="tab"
        aria-controls="v-tabs-user-docs"
        aria-selected="false"
        >User Documents</a
      >
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-office-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-office"
        role="tab"
        aria-controls="v-tabs-office"
        aria-selected="false"
        >Add new office</a
      >
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-new-user-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-new-user"
        role="tab"
        aria-controls="v-tabs-new-user"
        aria-selected="false"
        >Add new user</a
      >
    </div>
  </div>
  <div class="col-9">
    <!-- Tab content -->
    <div class="tab-content" id="v-tabs-tabContent">
      <div
        class="tab-pane fade show active"
        id="v-tabs-vacation-balance"
        role="tabpanel"
        aria-labelledby="v-tabs-vacation-balance-tab"
      >
        <div class="height-100">
          <GreatAndHint 
            hint={"You have to update the values every year"} 
            header={"this is vacation values of " + date.getFullYear()}
          />
          <VacationBalance />
        </div>
      </div>
      <div
        class="tab-pane fade"
        id="v-tabs-user-vacation-balance"
        role="tabpanel"
        aria-labelledby="v-tabs-user-vacation-balance-tab"
      >
        <div class="height-100">
          <GreatAndHint 
            header={"tThis is the user balance of year " + date.getFullYear()}
            hint={"The user also has an old balance object, we reset this old balance values to zeros on the first day of march month every year as a cron job, you can always check and if you find these values not zeros after `1/3/*years` you can delete all old balances by checking the checkbox below."} 
          />
          <UserVacationBalance />
        </div>
      </div>
      <div
      class="tab-pane fade"
      id="v-tabs-home"
      role="tabpanel"
      aria-labelledby="v-tabs-home-tab"
    >
      <div class="height-100">
        <GreatAndHint 
          header={"this is evaluation form of " + date.getFullYear()}
          hint={"Select quarter and link to make it visible to all of users."} 
        />
        <Evaluation />
      </div>
    </div>
    <div
      class="tab-pane fade"
      id="v-tabs-user-eval"
      role="tabpanel"
      aria-labelledby="v-tabs-user-eval-tab"
    >
      <div class="height-100">
        <GreatAndHint 
          header={"User evaluation form"}
          hint={"Add evaluation link to a specific user."} 
        />
        <UserEvaluation />
      </div>
    </div>
    <div
      class="tab-pane fade"
      id="v-tabs-user-docs"
      role="tabpanel"
      aria-labelledby="v-tabs-user-docs-tab"
    >
      <div class="height-100">
        <GreatAndHint 
          header={"User documents"}
          hint={"You can add any documents related to user by using this form."} 
        />
        <UserDocuments />
      </div>
    </div>
    <div
      class="tab-pane fade"
      id="v-tabs-office"
      role="tabpanel"
      aria-labelledby="v-tabs-office-tab"
    >
      <div class="height-100">
        <GreatAndHint 
          header={"New Office"}
          hint={"You can add office .e.g. `Codescalers` using this form."} 
        />
        <Office />
      </div>
    </div>
    <div
      class="tab-pane fade"
      id="v-tabs-new-user"
      role="tabpanel"
      aria-labelledby="v-tabs-new-user-tab"
    >
      <div>
        <GreatAndHint 
          header={"New User"}
          hint={"You can add new user using this form."} 
        />
        <Register />
      </div>
    </div>
    </div>
  </div>
</div>

<style>
  .nav{
      height: auto !important;
  }
  .navtab{
    padding: 15px;
    border-radius: 5px !important;
    transition: .3s;
  }
  .no-bottom-border{
    border-bottom: none;
  }
</style>














