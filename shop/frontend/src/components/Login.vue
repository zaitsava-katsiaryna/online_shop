<template>
    <div class="p-5">
        <h2 class="text-center p-3">Log In</h2>
        <b-form @submit="submitForm" class="w-25 mx-auto text-center" >
            <b-form-group
                    id="input-group-1"
                    label="Username:"
                    label-for="input-1"
            >
                <b-form-input
                        id="input-1"
                        v-model="form.email"
                        type="email"
                        required
                        placeholder="Enter email"
                ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Password:" label-for="input-2">
                <b-form-input
                        id="input-2"
                        v-model="form.password"
                        type="password"
                        required
                        placeholder="Enter password"
                ></b-form-input>
            </b-form-group>

            <b-button type="submit" variant="outline-success">Submit</b-button>


        </b-form>
        <div class="text-center m-5">Don't have an account yet?
            <span v-b-hover="handleHover" @click="redirect" :class="isHovered ? 'text-success cursor' : ''">Sign up</span></div>

        <b-alert
                :show="dismissCountDown"
                dismissible
                fade
                class="position-fixed fixed-top m-0 rounded-0 text-center"
                style="z-index: 2000;"
                :variant="alertVariant"
                @dismiss-count-down="countDownChanged"
        >
            {{alertMessage}}
        </b-alert>

    </div>
</template>

<script>

    import axios from 'axios'

        export default {
        data() {
            return {
                form: {
                    email: '',
                    password: '',
                },
                isHovered: false,
                dismissSecs: 2,
                dismissCountDown: 0,
                alertVariant: '',
                alertMessage: ''
            }
        },

        methods: {
            submitForm() {
                const path = 'http://localhost:5000/login';
                let credentials = {
                    email: this.form.email,
                    password: this.form.password
                };
                axios.post(path, credentials)
                    .then(res => {
                        localStorage.setItem('accessToken', res.data.access_token);
                        localStorage.setItem('username', res.data.username);
                        localStorage.setItem('userID', res.data.user_id);
                        this.dismissCountDown = this.dismissSecs;
                        this.alertMessage = 'Successfully logged in!';
                        this.alertVariant = 'success'

                    })
                    .catch(error => {
                        this.alertMessage = error.response.data.msg;
                        this.alertVariant = 'danger';
                        this.dismissCountDown = this.dismissSecs;
                    })
            },
            redirect() {
                this.$router.push('/signup');
            },
            handleHover(hovered) {
                this.isHovered = hovered
            },
            countDownChanged(dismissCountDown) {
                this.dismissCountDown = dismissCountDown;
                if (this.dismissCountDown === 0){
                    this.$router.push('/');
                }
            },
        }
    }
</script>

<style scoped>
    .cursor{
        cursor: pointer;
    }
</style>
