<template>
    <div class="p-5">
        <h2 class="text-center p-3">Sign Up</h2>
        <!-- <div class="text-center text-danger">{{error}}</div> -->
        <b-form @submit="submitForm" class="w-25 mx-auto text-center">
            <b-form-group id="input-group-1" label="Name:" label-for="input-1">
                <b-form-input
                        id="input-1"
                        v-model="form.name"
                        required
                        placeholder="John"

                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-2" label="Surname:" label-for="input-2">
                <b-form-input
                        id="input-2"
                        v-model="form.surname"
                        required
                        placeholder="Smith"
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-3" label="Email:" label-for="input-3">
                <b-form-input
                        id="input-3"
                        v-model="form.email"
                        type="email"
                        required
                        placeholder="example@mail.com"
                ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-4" label="Password:" label-for="input-4">
                <b-form-input
                        id="input-4"
                        v-model="form.password"
                        type="password"
                        required
                        placeholder="VeRy_SeCuRe_PaSsWoRd"
                ></b-form-input>
            </b-form-group>
            <b-button  type="submit" variant="outline-success">Submit</b-button>
        </b-form>
        <div class="text-center m-5">Already have an account?
            <span v-b-hover="handleHover" @click="redirect" :class="isHovered ? 'text-success cursor' : ''">Log in</span></div>

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
                    name: '',
                    surname: '',
                    email: '',
                    password: '',
                },
                isHovered: false,
                alertMessage: '',
                dismissSecs: 2,
                dismissCountDown: 0,
                alertVariant: ''

            }
        },

        methods: {
            submitForm() {
                const path = 'http://localhost:5000/signup';
                let user = {
                    name: this.form.name,
                    surname: this.form.surname,
                    email: this.form.email,
                    password: this.form.password
                };
                console.log(user);
                axios.post(path, user)
                    .then(() => {
                       this.dismissCountDown = this.dismissSecs;
                       this.alertMessage = 'Successfully signed up!';
                       this.alertVariant = 'success';
                    })
                    .catch(error => {
                        this.alertMessage = error.response.data.msg;
                        this.alertVariant = 'danger';
                        this.dismissCountDown = this.dismissSecs;
                    })
            },
            redirect() {
                this.$router.push('/login');
            },
            handleHover(hovered) {
                this.isHovered = hovered
            },
            countDownChanged(dismissCountDown) {
                this.dismissCountDown = dismissCountDown;
                if (this.dismissCountDown === 0){
                    this.redirect();
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
