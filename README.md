# Secure Customer-Bank Messaging System

## Overiview

- **Author:** Lawrence Galang
- **Student ID:** C3379933
- **Course:** SENG4400
- **Due Date:** 30/04/2026, 11:59am

## How to run

1.  Click the S3 Link Provided by AWS S3 Bucket
2.  Send Message as a Customer
3.  View Messages
    -   Either enetering a customer ID or not
4.  Reply to message as a staff
    -   Click on message to reply to it
5.  Reload messages to see the reply

## S3 Link (May Not Work After Submission)

http://secure-bank-messaging-bucket-lawrence.s3-website-us-east-1.amazonaws.com

## Architecture

This project implements a secure messaging system between customer and bank staff using AWS
and the following technology stack:

- **Frontend:** Static HTML, CSS, Javascript, hosted on AWS S3
- **API Gateway:** Handles HTTP requests
- **Backend:** AWS Lambda functions
- **Database:** DynamoDB
- **CI/CD:** GitHub Actions

## User Journey

1. Customer sends a message
2. Customer view message
3. Bank staff replies to a message

## Backend Modules

- **createMessage**
    - Handles new messages
- **getMessages**
    - Retrieves messages
- **replyMessage**
    - Handles staff replies


## API Route

- **POST** /messages
- **GET** /messages
- **GET** /messages/customerId
- **POST** /messages/{threadId}/reply

## Persistence

All mesages are stored in DynamoDB using a shared table accessed by all Lamba functions.

## CI/CD

GitHub Actions automatically deploys backend Lambda functions when code is pushed to the main branch.
