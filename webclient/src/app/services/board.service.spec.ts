import { TestBed, inject, async } from "@angular/core/testing";

import { BoardService } from "./board.service";
import { EveHttpService } from "./http.service";

import { Tile } from "../models/tile";
import { GameDto, Game } from "../models/game";
import { validateBoard } from "../models/game.spec";

describe("BoardService", () => {
    let httpService: EveHttpService;

    beforeEach(() => {
        httpService = {} as any;
        TestBed.configureTestingModule({
            providers: [
                BoardService
                , { provide: EveHttpService, useValue: httpService }
            ]
        });
    });

    it("should be created", inject([BoardService], (service: BoardService) => {
        expect(service).toBeTruthy();
    }));

    describe("getGames tests", () => {
        let get: Function;

        beforeEach(() => {
            httpService.get = ((...args) => get(args)) as any;
        });

        it("positive test, ordered", async(inject([BoardService], (service: BoardService) => {
            get = () => Promise.resolve({
                board: [
                    { x: 0, y: 0 }
                    , { x: 0, y: 1 }
                    , { x: 1, y: 0 }
                    , { x: 1, y: 1 }
                ]
            });

            return service.getGame("asd")
                .then(result => {
                    expect(result).toBeTruthy();
                    expect(result.board).toBeTruthy();
                    validateBoard(result.board, 2, 2);
                })
                .catch(e => {
                    fail(e);
                });
        })));

        it("positive test, reversed", async(inject([BoardService], (service: BoardService) => {
            get = () => Promise.resolve({
                board: [
                    { x: 1, y: 1 }
                    , { x: 1, y: 0 }
                    , { x: 0, y: 1 }
                    , { x: 0, y: 0 }
                ]
            });

            return service.getGame("asd")
                .then(result => {
                    expect(result).toBeTruthy();
                    expect(result.board).toBeTruthy();
                    validateBoard(result.board, 2, 2);
                })
                .catch(e => {
                    fail(e);
                });
        })));

        it("positive test, unordered", async(inject([BoardService], (service: BoardService) => {
            get = () => Promise.resolve({
                board: [
                    { x: 0, y: 1 }
                    , { x: 1, y: 1 }
                    , { x: 1, y: 0 }
                    , { x: 0, y: 0 }
                ]
            });

            return service.getGame("asd")
                .then(result => {
                    expect(result).toBeTruthy();
                    expect(result.board).toBeTruthy();
                    validateBoard(result.board, 2, 2);
                })
                .catch(e => {
                    fail(e);
                });
        })));
    });
});
