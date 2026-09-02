const app = require("./server");

describe("health endpoint", () => {
  it("reports that the API is running", () => {
    const route = app._router.stack.find(
      (layer) => layer.route && layer.route.path === "/health",
    );
    const json = jest.fn();

    route.route.stack[0].handle({}, { json });

    expect(json).toHaveBeenCalledWith(
      expect.objectContaining({ status: "API is running" }),
    );
  });
});
