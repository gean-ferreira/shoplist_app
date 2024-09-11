export interface LoginBase {
  username: string;
  password: string;
}

export interface LoginForm extends LoginBase {}

export interface LoginPayload extends LoginBase {}
