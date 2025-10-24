#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { PythonLambdaStack } from '../lib/python-lambda-stack';

const app = new cdk.App();

new PythonLambdaStack(app, 'PythonLambdaStack', {
  description: 'Python FastAPI Lambda API deployed with CDK',
});

app.synth();
