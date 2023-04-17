# Backend

Before comitting, ensure that your files are formatted with `black .`

## GatherReviewsLambda

Triggered by GatherReviewsQueue. Takes in the product_id from the queue. Webscrapes reviews and stores them in the reviews bucket. Can be run locally for development. It has a dependency on headless chrome and selenium which are added as a layer.

### Prerequisites

- Download headless chrome layer: https://github.com/diegoparrilla/headless-chrome-aws-lambda-layer/releases/tag/v0.2-beta.0
- Rename and upload `layer-headless_chrome.zip` to `artifacts-<ACCOUNT-ID>` bucket and under `gather-reviews-lamdba/` directory
