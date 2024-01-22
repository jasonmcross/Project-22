/*
  Warnings:

  - You are about to drop the `Employee` table. If the table is not empty, all the data it contains will be lost.

*/
-- CreateEnum
CREATE TYPE "patternGroup" AS ENUM ('Behavioral', 'Structural', 'Creational');

-- DropTable
DROP TABLE "Employee";

-- DropEnum
DROP TYPE "Role";

-- CreateTable
CREATE TABLE "patterns" (
    "patternId" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "group" "patternGroup" NOT NULL,
    "Collection" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "patterns_pkey" PRIMARY KEY ("patternId")
);
