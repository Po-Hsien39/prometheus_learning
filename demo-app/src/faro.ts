import { FetchInstrumentation } from "@grafana/faro-instrumentation-fetch";
import { XHRInstrumentation } from "@grafana/faro-instrumentation-xhr";
import {
  initializeFaro as coreInit,
  getWebInstrumentations,
} from "@grafana/faro-react";
import { TracingInstrumentation } from "@grafana/faro-web-tracing";
import type { Faro } from "@grafana/faro-react";

export function initializeFaro(): Faro {
  const instrumentationOptions = {
    propagateTraceHeaderCorsUrls: [
      new RegExp("https://demo-be.cony.line-apps.com"),
      new RegExp("http://localhost:4000"),
    ], // This is a list of specific URIs or regular exprressions
  };
  const faro = coreInit({
    url: "http://localhost:8027/collect",
    apiKey: "api_key",
    app: {
      name: "ocr-project",
      version: "1.0.0", // Optional, but recommended
    },
    instrumentations: [
      ...getWebInstrumentations({
        captureConsole: true,
      }),
      new FetchInstrumentation({}),
      new XHRInstrumentation({}),
      new TracingInstrumentation({ instrumentationOptions }),
    ],
  });

  faro.api.pushLog(["Faro was initialized"]);

  return faro;
}
